from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core import cache
from django.core.cache.backends import redis
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import CustomUser
from socialnet import settings


User = get_user_model()
redis_conn = get_redis_connection("default")

class StatusUserAPIView(APIView):
    def get(self, request, username, format=None):
        user_cache_key = 'last_seen_%s' % username
        last_seen = redis_conn.get(user_cache_key)
        print(user_cache_key,last_seen)
        if last_seen:
            last_seen = datetime.strptime(last_seen.decode('utf-8'), '%Y-%m-%d %H:%M:%S.%f')
            if (datetime.now() - last_seen) < timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                user_status = 'online'
            else:
                user_status = 'offline'
        else:
            user_status = 'offline'

        data = {'username': username, 'status': user_status,'last_seen':last_seen}
        return Response(data=data, status=status.HTTP_200_OK)
