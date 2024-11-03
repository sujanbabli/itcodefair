from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import uuid

# dashboard/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import uuid
from accounts.models import UserProfile  # Import UserProfile model



class Specialization(models.Model):
    """Model to manage different medical specializations"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# class Service(models.Model):
#     """Model to manage medical services"""
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     specialization = models.ForeignKey(
#         Specialization,
#         on_delete=models.CASCADE,
#         related_name='services'
#     )
#     image = models.ImageField(upload_to='services/', null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} "

class Doctor(models.Model):
    """Model for doctor profiles"""
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'DOCTOR'},  # Updated to match UserProfile choices
        related_name='doctor_profile'
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name='doctors'
    )
    name = models.CharField(max_length=200)  # Add name field
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(70)]
    )
    license_number = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='doctors/', null=True, blank=True)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    available_days = models.CharField(max_length=100)  # Store as "Mon,Tue,Wed"
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"Dr. {self.name}"  # Define get_full_name method to return full name with prefix "Dr."

    def __str__(self):
        return f"{self.get_full_name()} - {self.specialization}"

    class Meta:
        ordering = ['user__user__first_name']


class Patient(models.Model):
    """Model for patient profiles"""
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'CITIZEN'},
        related_name='patient_profile'
    )
    
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='patients'
    )
    
    name = models.CharField(max_length=100)
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        default=25,
    )
    phone = models.CharField(max_length=15)  # Added phone number field
    problem = models.TextField()
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Appointment(models.Model):
    """Model for managing appointments"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    appointment_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    problem_description = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient} with {self.doctor}"



class MedicalRecord(models.Model):
    """Model for storing medical records"""
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='medical_record',
        null=True,
        blank=True
    )
    diagnosis = models.TextField()
    prescription = models.TextField()
    lab_results = models.TextField(blank=True)
    next_visit_date = models.DateField(null=True, blank=True)
    attachments = models.FileField(upload_to='medical_records/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record - {self.patient} - {self.created_at.date()}"

class Schedule(models.Model):
    """Model for managing doctor schedules"""
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    reason = models.CharField(max_length=200, blank=True)  # For unavailability
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['doctor', 'date']

    def __str__(self):
        return f"{self.doctor} - {self.date}"
    

class Incident(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'CITIZEN'},  
        related_name='incidents'  
    )
    location = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident at {self.location} by {self.user.user.username}"
