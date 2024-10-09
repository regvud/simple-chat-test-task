from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from rest_framework import status


UserModel = get_user_model()


def get_user_by_id(user_id):
    user = UserModel.objects.filter(id=user_id).first()

    if user is None:
        raise APIException(
            f"User with id: {user_id} does not exist", code=status.HTTP_404_NOT_FOUND
        )
    return user
