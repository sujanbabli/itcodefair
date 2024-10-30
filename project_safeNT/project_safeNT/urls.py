"""
URL configuration for project_safeNT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_safeNT import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
    # Authentication Routes
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Admin Routes
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create_user/', views.create_user, name='create_user'),
    path('admin/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Doctor Routes
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/patients/', views.view_patients, name='view_patients'),
    path('doctor/appointments/', views.view_appointments, name='view_appointments'),
    path('doctor/availability/', views.update_availability, name='update_availability'),
    
    # Patient Routes
    path('patients/doctors/', views.view_doctors, name='view_doctors'),
    path('patients/request_appointment/<int:doctor_id>/', views.request_appointment, name='request_appointment'),
    path('patients/history/', views.view_medical_history, name='view_medical_history'),
    
    # Police Routes
    path('police/dashboard/', views.police_dashboard, name='police_dashboard'),
    path('police/cctv/', views.view_cctv, name='view_cctv'),
    
    # General Routes
    path('blank/', views.blank, name='blank'),
]
