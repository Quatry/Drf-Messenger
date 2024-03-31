from django.urls import path

from api.views import RegisterView, MessageListCreateAPIView, ChatListCreateAPIView, ChatMemberListCreateAPIView

urlpatterns = [
    path('api/register', RegisterView.as_view()),
    path('api/message', MessageListCreateAPIView.as_view()),
    path('api/chat', ChatListCreateAPIView.as_view()),
    path('api/chat_members', ChatMemberListCreateAPIView.as_view())
]
