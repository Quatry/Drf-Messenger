import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=120, null=False)
    bio = models.TextField(max_length=250)
    photo = models.ImageField(upload_to='profile_photos/',null=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()


class StatusUser(models.Model):
    CHOICES = [
        ('ONLINE', 'online'),
        ('OFFLINE', 'offline'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=CHOICES)


class Chat(models.Model):
    CHOICES = [
        ('SINGLE', 'Одиночный'),
        ('GROUP', 'Групповой'),
    ]
    name = models.CharField(max_length=30, null=False)
    type = models.CharField(choices=CHOICES)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class ChatMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    file = models.FileField(upload_to='chat_files/',null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date_sended = models.DateTimeField(auto_now_add=True)
