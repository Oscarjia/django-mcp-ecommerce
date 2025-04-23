from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.assistant_home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('generate/', views.generate_response, name='generate'),
]