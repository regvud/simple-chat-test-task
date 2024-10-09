from rest_framework import generics, status
from rest_framework.response import Response

from users.serializers import UserSerializer


class MeView(generics.GenericAPIView):
    """
    Method: GET

    Get information about authorized user.
    """

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
