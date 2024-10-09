from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
        )

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "email": {"required": True},
            "username": {"required": True},
        }
