from django.urls import path

from api.users.views import UserInfoRetrieveUpdateDestroyAPIView, StatusUserAPIView

urlpatterns = [
    path('<str:username>', UserInfoRetrieveUpdateDestroyAPIView.as_view()),
    path('status/<str:username>', StatusUserAPIView.as_view()),
]
