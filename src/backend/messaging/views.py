from rest_framework import viewsets, pagination

from .models import Message, ChatRoom
from .serializers import (MessageCreateSerializer, MessageSerializer,
                          ChatRoomCreateSerializer, ChatRoomSerializer)


class ChatRoomsViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()

    def get_serializer_class(self):
        if self.action.lower() in ("create", "update", "partial_update", "delete"):
            return ChatRoomCreateSerializer

        else:
            return ChatRoomSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MessagePaginator(pagination.PageNumberPagination):
    page_size = 50


class MessageViewSet(viewsets.ModelViewSet):
    pagination_class = MessagePaginator

    def get_serializer_class(self):
        if self.action.lower() in ("create", "update", "partial_update", "delete"):
            return MessageCreateSerializer

        else:
            return MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chat_room=self.kwargs['room_pk']).order_by("-created_at")

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, chat_room_id=self.kwargs['room_pk'])
