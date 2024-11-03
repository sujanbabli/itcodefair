from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('CITIZEN', 'Citizen'),   # Default role
        ('POLICE', 'Police'),
        ('DOCTOR', 'Doctor'),
        ('PENDING', 'Pending')    # Temporary role for verification purposes
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CITIZEN')
    intended_role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=17)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_pending(self):
        return self.role == 'PENDING'

    def __str__(self):
        return f"{self.user.username} - {self.intended_role}"
