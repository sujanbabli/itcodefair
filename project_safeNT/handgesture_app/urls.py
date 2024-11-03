from django.urls import path
from handgesture_app import views

urlpatterns = [
    path('hand-gesture/', views.hand_gesture_view, name='hand_gesture'),
    path('api/emergency/', views.emergency_request_view, name='emergency_request'),
]
