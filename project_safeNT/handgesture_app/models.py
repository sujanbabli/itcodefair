from django.db import models
from accounts.models import UserProfile

class EmergencyRequest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, default="Hand gesture detected: Open and Closed Fist")
    image = models.ImageField(upload_to='emergency_images/', null=True, blank=True) 
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency from {self.user.user.username} at {self.created_at}"

    class Meta:
        verbose_name = "Emergency Request"
        verbose_name_plural = "Emergency Requests"

