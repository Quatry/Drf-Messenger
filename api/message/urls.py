from django.urls import path

from api.message.views import MessageListCreateAPIView, MessageRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', MessageListCreateAPIView.as_view()),
    path('<int:pk>', MessageRetrieveUpdateDestroyAPIView.as_view()),
]
