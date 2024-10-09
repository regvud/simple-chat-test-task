from django.urls import path

from .views import (
    MessageListCreateView,
    MessageReadView,
    MessageRetrieveUpdateDestroyView,
    ThreadListCreateView,
    ThreadRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("threads", ThreadListCreateView.as_view(), name="thread-list-create"),
    path(
        "threads/<int:pk>",
        ThreadRetrieveUpdateDestroyView.as_view(),
        name="thread-retrieve-update-destroy",
    ),
    path(
        "threads/<int:pk>/messages",
        MessageListCreateView.as_view(),
        name="thread-messages",
    ),
    path(
        "messages/<int:pk>",
        MessageRetrieveUpdateDestroyView.as_view(),
        name="message-retrieve-update-destroy",
    ),
    path(
        "messages/<int:pk>/read",
        MessageReadView.as_view(),
        name="message-read",
    ),
]
