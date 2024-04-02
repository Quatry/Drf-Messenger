from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from api.views import RegisterView, MessageListCreateAPIView, ChatListCreateAPIView, ChatMemberListCreateAPIView, \
    MyTokenObtainPairView

urlpatterns = [
    path('api/register', RegisterView.as_view()),
    path('api/message', MessageListCreateAPIView.as_view()),
    path('api/chat', ChatListCreateAPIView.as_view()),
    path('api/chat_members', ChatMemberListCreateAPIView.as_view()),

    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout', TokenBlacklistView.as_view(), name='token_blacklist'),
]
