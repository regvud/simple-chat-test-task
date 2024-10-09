from django.urls import path

from .views import (
    UserRetrieveUpdateDestroyView,
    UserThreadsView,
    UserListCreateView,
    UserUnreadMessagesView,
)

urlpatterns = [
    path("", UserListCreateView.as_view(), name="user-list-create"),
    path(
        "<int:pk>",
        UserRetrieveUpdateDestroyView.as_view(),
        name="user-retrieve-update-destroy",
    ),
    path("<int:pk>/threads", UserThreadsView.as_view(), name="user-threads"),
    path(
        "<int:pk>/messages/unread", UserUnreadMessagesView.as_view(), name="user-unread-messages"
    ),
]
