from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.response import Response


from .crud import create_thread, get_thread_by_id, retrieve_existing_thread
from .models import Message, Thread
from .serializers import CreateThreadSerializer, MessageSerializer, ThreadSerializer


UserModel = get_user_model()


class ThreadListCreateView(generics.ListCreateAPIView):
    """
    Method: GET
    Retrieve paginated list of threads.

    Method: POST
    Create thread.
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return CreateThreadSerializer(*args, **kwargs)
        return ThreadSerializer(*args, **kwargs)

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        participants_ids = serializer.data["participants_ids"]
        participants = UserModel.objects.filter(id__in=participants_ids)

        existing_thread = retrieve_existing_thread(participants)
        if existing_thread:
            serialized_thread = self.serializer_class(existing_thread).data
            return Response(serialized_thread, status=200)

        new_thread = create_thread(participants)
        thread_serializer = self.serializer_class(new_thread).data

        return Response(thread_serializer, status=201)


class ThreadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, destroy thread
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    """
    Method: GET
    Retrieve paginated list of user messages.

    Method: POST
    Create message for thread, requires sender id in body of request.
    """

    serializer_class = MessageSerializer

    def get_queryset(self):
        thread_id = self.kwargs["pk"]
        get_thread_by_id(thread_id)

        return Message.objects.filter(thread_id=thread_id).all()

    def post(self, request, *args, **kwargs):
        data_serializer = self.get_serializer(data=self.request.data)
        data_serializer.is_valid(raise_exception=True)

        sender_id = data_serializer.data["sender"]

        thread_id = self.kwargs["pk"]
        thread = get_thread_by_id(thread_id)

        if not thread.participants.filter(id=sender_id).exists():
            raise APIException("This user cannot message in the current thread.")

        message_data = {
            "thread": thread_id,
            "sender": sender_id,
            "text": data_serializer.data["text"],
        }

        message_serializer = self.get_serializer(data=message_data)
        message_serializer.is_valid(raise_exception=True)

        message_serializer.save()

        return Response(message_serializer.data, status=201)


class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageReadView(generics.UpdateAPIView):
    """
    Method: PATCH
    Sets message is_read = True, if message not already read.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def patch(self, *args, **kwargs):
        message = self.get_object()

        if message.is_read:
            return Response(
                {"detail": f"Message {message.id} is already read."}, status=400
            )

        message.is_read = True
        message.save()

        return super().patch(*args, **kwargs)
