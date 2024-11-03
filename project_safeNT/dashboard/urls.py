from django.urls import path
from . import views



urlpatterns = [
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('police-dashboard/', views.police_dashboard, name='police_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('medical/', views.medical_services, name='medical_services'),
    path('specialist/<int:specialization_id>/', views.choose_specialist, name='choose_specialist'),
    path('report-incident/', views.report_incident, name='report_incident'),
    path('appointment/<int:doctor_id>/', views.appointment, name='appointment'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('doctor/create-profile/', views.create_doctor_profile, name='create_doctor_profile'),
    path('doctors/appointment/<uuid:appointment_id>/approve/', views.approve_appointment, name='approve_appointment'),
    path('doctors/appointment/<uuid:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('doctors/appointment/<uuid:appointment_id>/update/', views.update_appointment, name='update_appointment'),
    path('appointment/<int:appointment_id>/user_cancel/', views.user_cancel_appointment, name='user_cancel_appointment'),
    path('appointment/<int:appointment_id>/user_view/', views.user_view_appointment, name='user_view_appointment'),
    path('my-emergency-requests/', views.my_emergency_requests, name='my_emergency_requests'),
]
