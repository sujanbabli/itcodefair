from django.contrib import admin

from .models import User, Patient, CCTVFootage

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(CCTVFootage)

# Register your models here.
