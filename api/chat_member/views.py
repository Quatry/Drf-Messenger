from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.chat_member.serializers import ChatMemberSerializer
from api.models import ChatMember, Chat, CustomUser


class ChatMembersListAPI(generics.ListAPIView):
    """
    Список участников чата
    """
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        chat_members = ChatMember.objects.filter(chat=pk)
        serializer = ChatMemberSerializer(chat_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatMemberRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Получить/удалить участника чата
    """
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        chat_member = ChatMember.objects.get(id=pk)
        serializer = ChatMemberSerializer(chat_member, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatMemberListCreateAPIView(generics.ListCreateAPIView):
    """
    Добавить участника в чат
    """
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        chat = Chat.objects.get(id=request.data['chat'])
        user = CustomUser.objects.get(id=request.data['user'])
        # Проверка, состоит ли пользователь уже в чате
        # Проверка, можно ли добавить больше участников в одиночный чат
        if chat.type == 'SINGLE':
            current_members_count = ChatMember.objects.filter(chat=chat).count()
            if current_members_count >= 2:
                return Response("Нельзя добавить больше участников в чат", status=status.HTTP_400_BAD_REQUEST)
        existing_member = ChatMember.objects.filter(user=user, chat=chat).exists()
        if existing_member:
            return Response("Этот пользователь уже в чате.", status=status.HTTP_400_BAD_REQUEST)
        # Создание новой записи в модели ChatMember
        new_member = ChatMember(user=user, chat=chat)
        serializer = ChatMemberSerializer(new_member, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)