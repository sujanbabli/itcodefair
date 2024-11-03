from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from handgesture_app.models import EmergencyRequest
from accounts.models import UserProfile
import json

import base64
from django.core.files.base import ContentFile

@login_required
def hand_gesture_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role != 'CITIZEN':
        return HttpResponseForbidden("You are not authorized to send emergency requests.")
    
    if request.method == 'POST':
        data = json.loads(request.body)
        reason = data.get('reason', 'No reason provided')
        image_data = data.get('image', None)
        
        emergency_request = EmergencyRequest.objects.create(
            user=user_profile, 
            reason=reason, 
            created_at=timezone.now()
        )
        
        if image_data:
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1] 
            emergency_request.image = ContentFile(base64.b64decode(imgstr), name=f'emergency_{user_profile.id}.{ext}')
            emergency_request.save()
        
        return JsonResponse({'status': 'success', 'redirect_url': '/dashboard/my-emergency-requests/'})
    
    return render(request, 'handgesture_app/hand_gesture.html')

@login_required
def emergency_request_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reason = data.get('reason', 'No reason provided')
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.role == 'CITIZEN':
            # Create an emergency request in the database
            EmergencyRequest.objects.create(user=user_profile, reason=reason, created_at=timezone.now())
            # Send a confirmation response
            return JsonResponse({'status': 'success', 'message': 'Your emergency request has been sent successfully.'})
        
    return JsonResponse({'status': 'failed', 'message': 'Failed to send the emergency request.'}, status=400)