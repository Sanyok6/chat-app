from django.db.models.signals import post_save, pre_delete
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver

from .models import Message
from .serializers import MessageSerializer

channel_layer = get_channel_layer()


def dispatch_message_create(sender, instance, created, **kwargs):
    if created:
        async_to_sync(channel_layer.group_send)("chat", {"type": "message_create",
                                                         "payload": MessageSerializer(instance).data})

    else:
        async_to_sync(channel_layer.group_send)("chat", {"type": "message_update",
                                                         "payload": MessageSerializer(instance).data})


def dispatch_message_delete(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)("chat", {"type": "message_delete",
                                                     "payload": MessageSerializer(instance).data})


post_save.connect(dispatch_message_create, sender=Message, dispatch_uid="message_create_dispatcher")
pre_delete.connect(dispatch_message_delete, sender=Message, dispatch_uid="message_delete_dispatcher")
