from django.urls import path

from api.chat.views import ChatListCreateAPIView, ChatRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ChatListCreateAPIView.as_view()),
    path('<int:pk>', ChatRetrieveUpdateDestroyAPIView.as_view()),
]