from rest_framework import viewsets, pagination

from .models import Message
from .serializers import MessageCreateSerializer, MessageSerializer


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
        return Message.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
