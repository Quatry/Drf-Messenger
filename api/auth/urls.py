from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from api.auth.views import RegisterAPIView, LoginAPIView, MyTokenObtainPairView

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout', TokenBlacklistView.as_view(), name='token_blacklist')
]
