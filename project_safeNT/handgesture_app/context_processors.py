from handgesture_app.models import EmergencyRequest

def unseen_emergency_requests(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        if request.user.userprofile.role == 'police':
            unseen_count = EmergencyRequest.objects.filter(is_seen=False).count()
            return {'unseen_emergency_requests': unseen_count}
    return {'unseen_emergency_requests': 0}
