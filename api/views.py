from rest_framework import generics
from django.shortcuts import render
from rest_framework.permissions import AllowAny

from api.models import CustomUser, Message, Chat, ChatMember
from api.serializers import RegisterSerializer, MessageSerializer, ChatSerializer, ChatMemberSerializer


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


class ChatMemberListCreateAPIView(generics.ListCreateAPIView):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer


class AddChatMember(APIView):
    def post(self, request, chat_id, user_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            user = CustomUser.objects.get(id=user_id)

            # Проверка, состоит ли пользователь уже в чате
            existing_member = ChatMember.objects.filter(user=user, chat=chat).exists()
            if existing_member:
                return Response("Пользователь уже состоит в чате", status=status.HTTP_400_BAD_REQUEST)

            # Проверка, можно ли добавить больше участников в одиночный чат
            if chat.type == 'SINGLE':
                current_members_count = ChatMember.objects.filter(chat=chat).count()
                if current_members_count >= 2:
                    return Response("Нельзя добавить больше участников в чат", status=status.HTTP_400_BAD_REQUEST)

            # Создание новой записи в модели ChatMember
            new_member = ChatMember(user=user, chat=chat)
            new_member.save()

            serializer = ChatMemberSerializer(new_member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Chat.DoesNotExist:
            return Response("Чат не найден", status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)
