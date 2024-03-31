from django.urls import path

from api.views import RegisterView, MessageListCreateAPIView, ChatListCreateAPIView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('message', MessageListCreateAPIView.as_view()),
    path('chat', ChatListCreateAPIView.as_view()),
]
