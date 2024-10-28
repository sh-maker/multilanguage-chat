from django.urls import path
from .views import translate_message, get_messages

urlpatterns = [
    path('translate/', translate_message, name='translate_message'),  
    path('messages/', get_messages, name='get_messages'),
]
