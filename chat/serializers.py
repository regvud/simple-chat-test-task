from django.core.validators import MaxLengthValidator
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Message, Thread


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = Thread
        fields = ("id", "participants", "created", "updated")


class CreateThreadSerializer(serializers.Serializer):
    participants_ids = serializers.ListField(
        validators=[
            MaxLengthValidator(
                2, message="Thread cannot have more than 2 participants."
            )
        ]
    )


class MessageSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer
    sender = UserSerializer

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "thread",
            "text",
            "is_read",
            "created",
        )

        extra_kwargs = {
            "thread": {"required": False},
        }
