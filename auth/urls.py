from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from .views import MeView

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="obtain_tokens"),
    path("refresh", TokenRefreshView.as_view(), name="obtain_access"),
    path("me", MeView.as_view(), name="me_view"),
]
