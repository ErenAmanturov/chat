from django.db import models

from django.conf import settings

# Create your models here.
class Message(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    room_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.user} send {self.message}'

