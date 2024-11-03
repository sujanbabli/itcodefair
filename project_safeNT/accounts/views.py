from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from functools import wraps

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile

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
                    messages.error(request, "You don't have  permission to access this page.")
                    return redirect('index')  # Redirect to a page with permission error message
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('index')
            
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator

def index(request):
    """Landing page view."""   
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    return render(request, 'accounts/index.html')

@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already registered and logged in.")
        return redirect('index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(
                    request,
                    'Registration successful! Please log in with your credentials.'
                )
                return redirect('login')
            except Exception as e:
                messages.error(
                    request,
                    'An error occurred during registration. Please try again.'
                )
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@sensitive_post_parameters()
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            next_url = request.GET.get('next')
            if next_url and next_url.startswith('/'):  # Prevent open redirect
                return redirect(next_url)
            
            try:
                role = user.userprofile.role
                if role == 'POLICE':
                    return redirect('police_dashboard')
                elif role == 'DOCTOR':
                    return redirect('doctor_dashboard')
                elif role == 'CITIZEN':
                    return redirect('user_dashboard')
                else:
                    messages.info(request, "Please wait till your account is verified.")
                    return redirect('index')
            except UserProfile.DoesNotExist:
                return redirect('user_dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('index')

@login_required
@require_http_methods(["GET"])
def dashboard(request):
    try:
        role = request.user.userprofile.role
        if role == 'POLICE':
            return redirect('police_dashboard')
        elif role == 'DOCTOR':
            return redirect('doctor_dashboard')
        else:
            return redirect('user_dashboard')
    except UserProfile.DoesNotExist:
        messages.warning(request, "Profile not found. Please contact support.")
        return redirect('dashboard:user_dashboard')


@login_required
@require_http_methods(["GET"])
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'user_profile': profile,
        'role_display': profile.get_role_display(),
    }
    return render(request, 'accounts/profile.html', context)

# Error Handlers



