from django.urls import path

from api.users.views import UserInfoRetrieveUpdateDestroyAPIView, StatusUserAPIView, UserListAPIView

urlpatterns = [
    path('',UserListAPIView.as_view()),
    path('<str:username>', UserInfoRetrieveUpdateDestroyAPIView.as_view()),
    path('status/<str:username>', StatusUserAPIView.as_view()),
]
