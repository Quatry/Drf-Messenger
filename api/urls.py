from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('user/', include('api.users.urls')),
    path('chat/', include('api.chat.urls')),
    path('chat_members/', include('api.chat_member.urls')),
    path('message/', include('api.message.urls'))
]
