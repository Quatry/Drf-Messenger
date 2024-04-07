from datetime import datetime, timedelta

import redis
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class ActiveUserMiddleware(JWTAuthentication):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        now = datetime.now()
        if request.user.is_authenticated:
            current_user = request.user
            user_cache_key = 'last_seen_%s' % current_user.username
            cache.set(user_cache_key, now, settings.USER_LASTSEEN_TIMEOUT)
            print(cache.get(user_cache_key),111)
        else:
            last_seen = cache.get('status')
            if last_seen and (now - last_seen) > timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                # Пользователь неактивен в течение USER_ONLINE_TIMEOUT секунд, переводим его в оффлайн
                cache.set('status', now, settings.USER_LASTSEEN_TIMEOUT)
                if request.COOKIES.get('sessionid'):
                    # Работа с сессиями, если необходимо
                    pass
            else:
                cache.set('status', now, settings.USER_LASTSEEN_TIMEOUT)
        return response