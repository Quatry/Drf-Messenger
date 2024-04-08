from django.urls import path

from api.chat_member.views import ChatMembersListAPI, ChatMemberListCreateAPIView, ChatMemberRetrieveDestroyAPIView

urlpatterns = [
    path('chat/<int:pk>/', ChatMembersListAPI.as_view()),
    path('', ChatMemberListCreateAPIView.as_view()),
    path('<int:pk>', ChatMemberRetrieveDestroyAPIView.as_view()),
]
