from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from api.views import RegisterView, MessageListCreateAPIView, ChatListCreateAPIView, ChatMemberListCreateAPIView, \
    MyTokenObtainPairView, ChatRetrieveUpdateDestroyAPIView, ChatMembersListAPI, ChatMemberRetrieveDestroyAPIView

urlpatterns = [
    path('api/register', RegisterView.as_view()),
    path('api/message', MessageListCreateAPIView.as_view()),
    path('api/chat', ChatListCreateAPIView.as_view()),
    path('api/chat/<int:pk>', ChatRetrieveUpdateDestroyAPIView.as_view()),
    path('api/chat/<int:pk>/members', ChatMembersListAPI.as_view()),
    path('api/chat_members', ChatMemberListCreateAPIView.as_view()),
    path('api/chat_members/<int:pk>', ChatMemberRetrieveDestroyAPIView.as_view()),

    path('api/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout', TokenBlacklistView.as_view(), name='token_blacklist'),
]
