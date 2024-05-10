from django.urls import path, include
from api.auth.views import RegisterAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('', include('rest_framework.urls')),
]
