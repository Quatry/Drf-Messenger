from rest_framework import generics
from django.shortcuts import render
from rest_framework.permissions import AllowAny

from api.models import CustomUser, Message, Chat
from api.serializers import RegisterSerializer, MessageSerializer, ChatSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ChatListCreateAPIView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer