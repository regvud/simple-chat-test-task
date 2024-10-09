from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import make_password
from rest_framework import generics

from django.db.models import Q
from chat.models import Message, Thread
from chat.serializers import MessageSerializer, ThreadSerializer
from users.crud import get_user_by_id

from .serializers import UserSerializer


UserModel = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    """
    Method: GET
    Retrieve paginated list of users.

    Method: POST
    Create user.
    """

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        if "password" in data:
            data["password"] = make_password(data["password"])

        return super().create(request, *args, **kwargs)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, destroy user.
    """

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserThreadsView(generics.ListAPIView):
    """
    Method GET:
    Retrieve paginated threads for user.
    """

    serializer_class = ThreadSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs["pk"]
        user = get_user_by_id(user_id)

        return Thread.objects.filter(participants=user).all()


class UserUnreadMessagesView(generics.ListAPIView):
    """
    Method GET:
    Retrieve paginated unread messages for user.
    """

    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        get_user_by_id(user_id)

        return Message.objects.filter(Q(sender_id=user_id) & Q(is_read=False)).all()
