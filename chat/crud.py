from rest_framework.exceptions import APIException
from rest_framework import status
from chat.models import Thread


def get_thread_by_id(thread_id):
    thread = Thread.objects.filter(id=thread_id).first()

    if thread is None:
        raise APIException(
            f"Thread with id: {thread_id} does not exist.",
            code=status.HTTP_404_NOT_FOUND,
        )
    return thread


def retrieve_existing_thread(user_queryset):
    threads = Thread.objects.filter(participants__in=user_queryset).distinct()

    for thread in threads:
        if set(thread.participants.all()) == set(user_queryset.all()):
            return thread
    return None


def create_thread(participants):
    MAX_THREAD_PARTICIPANTS = 2

    if participants.count() > MAX_THREAD_PARTICIPANTS:
        raise APIException(
            f"Thread cannot have more than {MAX_THREAD_PARTICIPANTS} participants.",
            code=status.HTTP_400_BAD_REQUEST,
        )

    if participants.count() == 0:
        raise APIException(
            "Thread should have at least 1 participant.",
            code=status.HTTP_400_BAD_REQUEST,
        )

    new_thread = Thread.objects.create()
    new_thread.participants.set(participants)

    return new_thread
