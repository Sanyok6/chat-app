import json

from asgiref.sync import async_to_sync
from authentication.serializers import UserSerializer
from channels.generic.websocket import WebsocketConsumer

from .models import ChatRoom
from .serializers import ChatRoomSerializer


def get_ready_event_payload(user, *, k_user_data="user", k_public_chats="public_chats"):
    return {
        k_user_data: UserSerializer(user).data,
        k_public_chats: ChatRoomSerializer(ChatRoom.objects.filter(is_public=True), many=True).data,
    }


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            return self.close(401) # Not Authenticated

        self.chat_room_name = self.scope['url_route']['kwargs']['room_name']

        if not ChatRoom.objects.filter(id=self.chat_room_name).exists():
            return self.close(404) # Not Found

        async_to_sync(self.channel_layer.group_add)(
            self.chat_room_name,
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
            self.chat_room_name,
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
