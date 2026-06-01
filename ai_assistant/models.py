from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat sessiyasi"
        verbose_name_plural = "Chat sessiyalari"
        ordering = ['-created_at']


class ChatMessage(models.Model):
    ROLE_CHOICES = [('user', 'Foydalanuvchi'), ('assistant', 'Yordamchi')]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat xabari"
        verbose_name_plural = "Chat xabarlari"
        ordering = ['created_at']
