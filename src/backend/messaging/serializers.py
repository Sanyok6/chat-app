from rest_framework import serializers

from authentication.serializers import UserSerializer
from . import models


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ('author', 'content')


class MessageSerializer(MessageCreateSerializer):
    author = UserSerializer()

    class Meta(MessageCreateSerializer.Meta):
        fields = '__all__'
