from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.message.serializers import MessageSerializer
from api.models import Message, Chat, ChatMember


class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    Создать сообщение или получить список всех сообщений
    """
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


class MessageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, ]

z