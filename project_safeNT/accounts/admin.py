from django.contrib import admin

# Register your models here.
from accounts.models import UserProfile

# Register your models here.
from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role','intended_role' ,'phone_number', 'address', 'created_at', 'updated_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'role')
    ordering = ('user',)
    fields = ('user', 'role','phone_number', 'address')

admin.site.register(UserProfile, UserProfileAdmin)