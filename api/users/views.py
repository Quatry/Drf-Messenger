from datetime import datetime, timedelta
from django.core.cache import cache
from django_redis import get_redis_connection
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import CustomUser
from api.users.serializers import CustomUserSerializer
from socialnet import settings

redis_conn = get_redis_connection("default")


class UserInfoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Информация о пользователе
    """
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
            if user:
                serializer = CustomUserSerializer(user, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

class StatusUserAPIView(APIView):
    """
    Информация о статусе пользователя (online/offline)
    """
    def get(self, request, username, format=None):
        user_cache_key = 'last_seen_%s' % username
        last_seen = cache.get(user_cache_key)
        if last_seen:
            if (datetime.now() - last_seen) < timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                user_status = 'online'
                data = {'username': username, 'status': user_status}
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                user_status = 'offline'
                data = {'username': username, 'status': user_status, 'last_seen': last_seen}
                return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {'username': username, 'status': 'offilne', 'last_seen': 'Более недели назад'}
            return Response(data=data, status=status.HTTP_200_OK)
