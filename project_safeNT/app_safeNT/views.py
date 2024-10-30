from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User, Patient, CCTVFootage
from .forms import UserRegistrationForm, PatientForm

def is_doctor(user):
    return user.user_type == 'doctor'

def is_police(user):
    return user.user_type == 'police'

def is_admin(user):
    return user.user_type == 'admin'

def home(request):
    return render(request, 'app_safeNT/index.html')

# Doctor's dashboard to view and manage patients
@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    patients = Patient.objects.filter(doctor=request.user)
    return render(request, 'app_safeNT/doctor_dashboard.html', {'patients': patients})

@login_required
@user_passes_test(is_doctor)
def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'app_safeNT/view_patient.html', {'patient': patient})

@login_required
@user_passes_test(is_doctor)
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient information updated successfully.")
            return redirect('doctor_dashboard')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'app_safeNT/edit_patient.html', {'form': form})

# Police dashboard to view CCTV footage
@login_required
@user_passes_test(is_police)
def police_dashboard(request):
    footages = CCTVFootage.objects.all()
    return render(request, 'app_safeNT/police_dashboard.html', {'footages': footages})

# Admin dashboard to manage users
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'app_safeNT/admin_dashboard.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('admin_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'app_safeNT/create_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('admin_dashboard')

@login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'app_safeNT/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
