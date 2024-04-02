from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import CustomUser, Message, Chat, ChatMember
from api.serializers import RegisterSerializer, MessageSerializer, ChatSerializer, ChatMemberSerializer, \
    MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        chat = Chat.objects.get(id=request.data['chat'])
        user = request.user

        if ChatMember.objects.filter(user=user, chat=chat).exists():
            data = {
                'chat': chat.id,
                'user': user.id,
                'body': request.data['body'],
            }
            if request.data['file']:
                data['file'] = request.data['file']
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Пользователь не состоит в этом чате', status=status.HTTP_400_BAD_REQUEST)


class ChatListCreateAPIView(generics.ListCreateAPIView):
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
    lookup_field = 'pk'
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        message = Message.objects.filter(chat=pk)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatMemberListCreateAPIView(generics.ListCreateAPIView):
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


class ChatMemberRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        chat_member = ChatMember.objects.get(id=pk)
        serializer = ChatMemberSerializer(chat_member, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatMembersListAPI(generics.ListAPIView):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        chat_members = ChatMember.objects.filter(chat=pk)
        serializer = ChatMemberSerializer(chat_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
