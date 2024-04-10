from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from api.auth.views import RegisterAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('', include('rest_framework.urls')),
    # path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/logout', TokenBlacklistView.as_view(), name='token_blacklist')
]
