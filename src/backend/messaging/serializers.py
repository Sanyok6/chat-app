from rest_framework import serializers

from authentication.serializers import UserSerializer
from . import models


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatRoom
        fields = ('name', 'description', 'is_public')


class ChatRoomSerializer(ChatRoomCreateSerializer):
    creator = UserSerializer()
    class Meta(ChatRoomCreateSerializer.Meta):
        fields = '__all__'


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ('author', 'content')


class MessageSerializer(MessageCreateSerializer):
    author = UserSerializer()

    class Meta(MessageCreateSerializer.Meta):
        fields = '__all__'
