from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.chat.serializers import ChatSerializer
from api.chat_member.serializers import ChatMemberSerializer
from api.message.serializers import MessageSerializer
from api.models import Chat, ChatMember, Message


class ChatListCreateAPIView(generics.ListCreateAPIView):
    """
    Создать чат или получить список всех чатов
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        data = {
            'name': request.data['name'],
            'type': request.data['type'],
            'creator': request.user.id,
        }
        serializer = ChatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            chat = serializer.instance
            user = request.user
            chat_member = ChatMember(user=user, chat=chat)
            data = {
                'user': user.id,
                'chat': chat.id,
            }
            chat_member_serializer = ChatMemberSerializer(chat_member, data=data)
            if chat_member_serializer.is_valid():
                chat_member_serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить/обновить/удалить чат
    """
    lookup_field = 'pk'
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        message = Message.objects.filter(chat=pk)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChatListAPIView(generics.ListAPIView):
    lookup_field = 'username'
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChatSerializer

    def list(self, request, *args, **kwargs):
        member = ChatMember.objects.filter(user=request.user.id).order_by('date_joined').all()
        serializer_member = ChatMemberSerializer(member, many=True)
        return Response(serializer_member.data, status=status.HTTP_200_OK)
