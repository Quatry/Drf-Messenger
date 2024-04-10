from datetime import datetime, timedelta

from django.core.cache import cache
from django.conf import settings

class ActiveUserMiddleware:
    """
    Middleware отслеживающий когда пользователь был активен
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        now = datetime.now()
        if request.user.is_authenticated:
            current_user = request.user
            user_cache_key = 'last_seen_%s' % current_user.username
            cache.set(user_cache_key, now, settings.USER_LASTSEEN_TIMEOUT)
        return response
