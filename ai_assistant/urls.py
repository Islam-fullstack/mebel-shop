from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='ai_chat'),
    path('chat/yuborish/', views.send_message, name='send_message'),
    path('chat/tozalash/', views.clear_chat, name='clear_chat'),
]
