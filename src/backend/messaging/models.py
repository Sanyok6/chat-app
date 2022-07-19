import datetime
from django.db import models
from django.conf import settings

from django.utils.crypto import get_random_string


def generate_room_id():
    return get_random_string(20)

class ChatRoom(models.Model):
    id = models.SlugField(allow_unicode=True, primary_key=True, default=generate_room_id)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.edited_at = datetime.datetime.utcnow()

        return super().save(*args, **kwargs)
