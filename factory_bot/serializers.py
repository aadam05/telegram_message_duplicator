from rest_framework import serializers
from .models import TelegramUser, Message


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_text']
