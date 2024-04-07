from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from socialnet import settings

User = get_user_model()
redis_conn = get_redis_connection("default")

class StatusUserAPIView(APIView):
    def get(self, request, username, format=None):
        user_cache_key = 'last_seen_%s' % username
        last_seen = cache.get(user_cache_key)
        print(user_cache_key, last_seen)
        if last_seen:
            if (datetime.now() - last_seen) < timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                user_status = 'online'
            else:
                user_status = 'offline'
        else:
            user_status = 'offline'

        data = {'username': username, 'status': user_status, 'last_seen': last_seen}
        return Response(data=data, status=status.HTTP_200_OK)
