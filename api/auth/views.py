from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.serializers import RegisterSerializer, LoginSerializer, MyTokenObtainPairSerializer
from api.models import CustomUser


class RegisterAPIView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)  # Создание Refesh и Access

            refresh.payload.update({  # Полезная информация в самом токене

                'user_id': str(user.id),

                'username': user.username

            })
            print(request.headers)

            return Response({

                'refresh': str(refresh),

                'access': str(refresh.access_token),  # Отправка на клиент

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     """
#     Логин
#     """
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny, ]
#
#     def post(self, request):
#
#         data = request.data
#
#         username = data.get('username', None)
#
#         password = data.get('password', None)
#
#         if username is None or password is None:
#             return Response({'error': 'Нужен и логин, и пароль'},
#
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         user = authenticate(username=username, password=password)
#
#         if user is None:
#             return Response({'error': 'Неверные данные'},
#
#                             status=status.HTTP_401_UNAUTHORIZED)
#
#         refresh = RefreshToken.for_user(user)
#
#         refresh.payload.update({
#
#             'user_id': str(user.id),
#
#             'username': user.username
#
#         })
#
#         return Response({
#
#             'refresh': str(refresh),
#
#             'access': str(refresh.access_token),
#
#         }, status=status.HTTP_200_OK)
#
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
