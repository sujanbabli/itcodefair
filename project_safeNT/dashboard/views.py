from datetime import datetime, timedelta
import json
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from functools import wraps
from django.http import HttpResponseRedirect

from handgesture_app.models import EmergencyRequest

from .forms import AppointmentForm, DoctorProfileForm, IncidentForm, PatientForm

from .models import Specialization, Doctor, Appointment

from .models import Doctor, UserProfile

def role_required(roles):
    """
    Decorator for views that checks whether a user has a particular role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please login to access this page.")
                return redirect(f"{reverse('login')}?next={request.path}")
            
            try:
                user_profile = request.user.userprofile
                if user_profile.role not in roles:
                    messages.error(request, "You don't have permission to access this page.")
                    return redirect('index')  # Redirect to a page with permission error message
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('index')
            
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator

@login_required
def user_dashboard(request):
    """User dashboard displaying all doctor appointments."""
    profile = get_object_or_404(UserProfile, user=request.user)


    if profile.role == 'CITIZEN':
        appointments = Appointment.objects.filter(patient__user=request.user.userprofile).select_related('doctor')
        context = {
            'user_profile': profile,
            'appointments': appointments,
        }
        return render(request, 'dashboard/user_dashboard.html', context)
    
    if profile.role == 'POLICE':
        return redirect('police_dashboard')
    if profile.role == 'DOCTOR':
        return redirect('doctor_dashboard')
    if profile.role == 'PENDING':
        return render(request, 'dashboard/pending.html',{'user_profile': profile})
        
    return render(request, 'dashboard/user_dashboard.html')





@login_required
def user_cancel_appointment(request, appointment_id):
    """Allows a user to cancel an appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user.userprofile)

    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'The appointment has been canceled.')
    else:
        messages.error(request, 'This appointment cannot be canceled.')

    return redirect('user_dashboard')


@login_required
def user_view_appointment(request, appointment_id):
    """View details of a completed appointment, including prescription and notes."""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user.userprofile)

    if appointment.status == 'completed':
        context = {
            'appointment': appointment,
        }
        return render(request, 'dashboard/user_view_appointment.html', context)
    
    messages.error(request, 'Only completed appointments can be viewed.')
    return redirect('user_dashboard')
  
    



@login_required
@role_required(['DOCTOR'])
@require_http_methods(["GET"])
def doctor_dashboard(request):



    try:
        profile = get_object_or_404(UserProfile, user=request.user)
        doctor = profile.doctor_profile
    except Doctor.DoesNotExist:
        return redirect(reverse('create_doctor_profile'))
    
    
   
    
    
    
    today = timezone.now().date()
    
    total_patients = doctor.appointments.values('patient').distinct().count()
    today_appointments = doctor.appointments.filter(
        appointment_date=today,
        status='confirmed'
    ).count()
    this_week = doctor.appointments.filter(
        appointment_date__range=[today, today + timezone.timedelta(days=7)],
        status='confirmed'
    ).count()
    completed_count = doctor.appointments.filter(status='completed').count()
    total_count = doctor.appointments.count()
    completion_rate = (completed_count / total_count * 100) if total_count > 0 else 0
    
    pending_appointments = doctor.appointments.filter(
        status='pending'
    ).select_related('patient')
    
    upcoming_appointments = doctor.appointments.filter(
        status='confirmed',
        appointment_date__gte=today
    ).select_related('patient')
    
    completed_appointments = doctor.appointments.filter(
        status='completed'
    ).select_related('patient').order_by('-updated_at')[:5]
    
    context = {
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'this_week': this_week,
        'completion_rate': f"{completion_rate:.0f}",
        'pending_appointments': pending_appointments,
        'upcoming_appointments': upcoming_appointments,
        'completed_appointments': completed_appointments,
        'user_profile': profile
    }
    
    return render(request, 'dashboard/doctor_dashboard.html', context)



@login_required
@role_required(['DOCTOR'])
def create_doctor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    # If the profile already exists, redirect to the dashboard
    if hasattr(profile, 'doctor_profile'):
        return HttpResponseRedirect(reverse('doctor_dashboard'))
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = profile  # Associate with current user's profile
            doctor.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorProfileForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/create_doctor_profile.html', context)

@login_required
@role_required(['CITIZEN'])
@require_http_methods(["GET"])
def medical_services(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    specializations = Specialization.objects.all()
    context = {
        'specializations': specializations,
        'user_profile': profile,
    }
    
    return render(request, 'dashboard/medical_services.html', context)


@login_required
@role_required(['CITIZEN'])
@require_http_methods(["GET"])
def choose_specialist(request, specialization_id):
    specialization = get_object_or_404(Specialization, id=specialization_id)
    doctors = Doctor.objects.filter(specialization=specialization, is_active=True)
    context = {
        'specialization': specialization,
        'doctors': doctors,
    }
    return render(request, 'dashboard/choose_specialist.html', context)


def generate_time_slots(start_time, end_time, interval=60):
    """Generates a list of time slots between start and end times with a specified interval, formatted with AM/PM."""
    slots = []
    base_date = datetime.today().date()
    start_datetime = datetime.combine(base_date, start_time)
    end_datetime = datetime.combine(base_date, end_time)

    current_time = start_datetime
    while current_time < end_datetime:
        slots.append(current_time.strftime("%I:%M %p"))  # Format with AM/PM
        current_time += timedelta(minutes=interval)
    return slots


@login_required
@role_required(['CITIZEN'])
@require_http_methods(["GET"])
def appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    available_slots = generate_time_slots(doctor.available_time_start, doctor.available_time_end)
    return render(request, 'dashboard/appointment.html', {'doctor': doctor, 'available_slots': available_slots})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient

@login_required
@role_required(['CITIZEN'])
@require_http_methods(["POST"])
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        problem = request.POST.get('problem')
        medical_history = request.POST.get('history')
        appointment_date = request.POST.get('appointment_date')
        appointment_time_str = request.POST.get('time')

        try:
            appointment_time = datetime.strptime(appointment_time_str, '%I:%M %p').time()
        except ValueError:
            messages.error(request, 'Invalid time format. Please use HH:MM AM/PM format.')
            return redirect('your_appointment_page') 
        
        if Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date, appointment_time=appointment_time).exists():
            messages.error(request, 'This time slot is already booked. Please choose a different time.')
            return redirect('book_appointment', doctor_id=doctor_id)

        patient, created = Patient.objects.get_or_create(
            user=request.user.userprofile,  # assuming userprofile exists
            defaults={
                'doctor': doctor,
                'name': name,
                'age': age,
                'phone': phone,
                'problem': problem,
                'medical_history': medical_history,
            }
        )
        
        if not created:
            patient.name = name
            patient.age = age
            patient.phone = phone
            patient.problem = problem
            patient.medical_history = medical_history
            patient.save()

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            problem_description=problem,
            status='pending'
        )

        messages.success(request, 'Your appointment has been successfully booked.')
        return redirect('user_dashboard') 
    
    return render(request, 'dashboard/user_dashboard.html', {'doctor': doctor})


@login_required
@role_required(['DOCTOR'])
@require_http_methods(["POST"]) # Ensures only POST requests are allowed
def approve_appointment(request, appointment_id):
    messages.success(request, 'approved appointment')
    profile = get_object_or_404(UserProfile, user=request.user)
    doctor = profile.doctor_profile
    try:
        appointment = Appointment.objects.get(
            appointment_id=appointment_id,
            doctor=doctor,
            status='pending'
        )
        appointment.status = 'confirmed'
        appointment.save()
        return JsonResponse({'status': 'success'})
    except Appointment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Appointment not found'}, status=404)

@login_required
@role_required(['DOCTOR'])
@require_http_methods(["POST"]) 
def cancel_appointment(request, appointment_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    doctor = profile.doctor_profile
    try:
        appointment = Appointment.objects.get(
            appointment_id=appointment_id,
            doctor=doctor
        )
        appointment.status = 'cancelled'
        appointment.save()
        return JsonResponse({'status': 'success'})
    except Appointment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Appointment not found'}, status=404)

@login_required
@role_required(['DOCTOR'])
@require_http_methods(["POST"]) 
def update_appointment(request, appointment_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    doctor = profile.doctor_profile
    
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        appointment = Appointment.objects.get(
            appointment_id=appointment_id,
            doctor=doctor
        )
        
        # Update fields with the parsed JSON data
        appointment.prescription = data.get('prescription', '')
        appointment.notes = data.get('notes', '')
        appointment.status = 'completed'
        appointment.save()

        return JsonResponse({'status': 'success'})
        
    except Appointment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Appointment not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    


@login_required
def report_incident(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.user = request.user.userprofile  # Assuming user is linked correctly
            incident.save()
            # Add a success message to be displayed on the same page
            messages.success(request, 'Your report has been submitted. We will contact you soon.')
            form = IncidentForm()  # Clear the form after successful submission
    else:
        form = IncidentForm()
    context = {
        'user_profile': user_profile,
        'form': form    
    }
    return render(request, 'dashboard/report.html', context)
from .models import Incident


@login_required
@role_required(['POLICE'])
def police_dashboard(request):
    """Police dashboard with emergency monitoring."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        emergency_request = get_object_or_404(EmergencyRequest, id=request_id)
        # Toggle the is_seen status
        emergency_request.is_seen = not emergency_request.is_seen
        emergency_request.save()
        # Redirect to reload the page
        return redirect('police_dashboard')
    
    emergency_requests = EmergencyRequest.objects.all().order_by('-created_at')
    incidents = Incident.objects.all().order_by('-created_at')
    context = {
        'user_profile': user_profile,
        'emergency_requests': emergency_requests,
        'incidents': incidents,
    }
    return render(request, 'dashboard/police_dashboard.html', context)


@login_required
@role_required('CITIZEN')
def my_emergency_requests(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    emergency_requests = EmergencyRequest.objects.filter(user=user_profile).order_by('-created_at')
    incidents = Incident.objects.filter(user=user_profile).order_by('-created_at')
    
    context = {
        'user_profile': user_profile,
        'emergency_requests': emergency_requests,
        'incidents': incidents
    }
    return render(request, 'dashboard/my_emergency_requests.html', context)

# Create your views here.
