from django.contrib import admin
from .models import Incident, Specialization, Doctor, Patient, Appointment, MedicalRecord, Schedule

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'specialization', 'license_number', 'is_active')
    list_filter = ('specialization', 'is_active')
    search_fields = ('user__user__first_name', 'user__user__last_name', 'license_number', 'name')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'age', 'doctor', 'problem', 'medical_history')
    list_filter = ('age',)
    search_fields = ('user__user__first_name', 'user__user__last_name', 'name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('appointment_id', 'patient__user__user__first_name', 'doctor__user__user__first_name', 'status')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at', 'diagnosis', 'next_visit_date')
    list_filter = ('next_visit_date',)
    search_fields = ('patient__user__user__first_name', 'doctor__user__user__first_name', 'diagnosis')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'is_available', 'reason')
    list_filter = ('is_available', 'date')
    search_fields = ('doctor__user__user__first_name', 'doctor__user__user__last_name', 'reason')


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at', 'message')
    list_filter = ('created_at',)
    search_fields = ('location', 'user__user__username')

