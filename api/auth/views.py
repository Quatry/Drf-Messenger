from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.auth.serializers import RegisterSerializer
from api.models import CustomUser


class RegisterAPIView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
