import json

from asgiref.sync import async_to_sync
from authentication.serializers import UserSerializer
from channels.generic.websocket import WebsocketConsumer

from .models import Message
from .serializers import MessageSerializer


def get_ready_event_payload(user, *, user_data_key="user"):
    return {
        user_data_key: UserSerializer(user).data
    }


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            self.close(401) # Not Authenticated
            return

        async_to_sync(self.channel_layer.group_add)(
            "chat",
            self.channel_name
        )

        user.is_online = True
        user.save()

        self.accept()

        self.dispatch_named_event("READY", get_ready_event_payload(user))

    def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_anonymous:
            return

        async_to_sync(self.channel_layer.group_discard)(
            "chat",
            self.channel_name
        )

        user.is_online = False
        user.save()

    def dispatch_named_event(self, event_name, payload, extra_params={}):
        """A helper function to dispatch an event with a name specified"""

        data = {
            "event": event_name.upper(),
            "payload": payload,
            **extra_params
        }
        self.send(text_data=json.dumps(data))

    def message_create(self, event):
        self.dispatch_named_event("MESSAGE_CREATE", event["payload"])

    def message_update(self, event):
        self.dispatch_named_event("MESSAGE_UPDATE", event["payload"])

    def message_delete(self, event):
        self.dispatch_named_event("MESSAGE_DELETE", event["payload"])

    def user_update(self, event):
        self.dispatch_named_event("USER_UPDATE", event["payload"])
