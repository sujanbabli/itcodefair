from django.db import models
from django.contrib.auth.models import AbstractUser

# Define User model with role-based permissions
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Doctor'),
        (3, 'Police'),
        (4, 'User'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# Model for Doctors to manage patients
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 4})
    assigned_doctor = models.ForeignKey(User, related_name='patients', limit_choices_to={'user_type': 2}, on_delete=models.SET_NULL, null=True, blank=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Availability and notification management for doctors
class DoctorAvailability(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 2})
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.username} - {'Available' if self.is_available else 'Not Available'}"

class AppointmentRequest(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 4})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 2})
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.patient.username} to {self.doctor.username} - {self.status}"

# Model for Police access to CCTV
class CCTVFootage(models.Model):
    location = models.CharField(max_length=255)
    footage_url = models.URLField()
    alert_signal = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {'Alert' if self.alert_signal else 'No Alert'}"

# Admin management of users
class AdminControl(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 1})
    action_performed = models.CharField(max_length=255)
    performed_on = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin {self.admin.username} performed action on {self.performed_on.username}"
