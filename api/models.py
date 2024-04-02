import uuid
from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.cache import cache

from socialnet import settings


class CustomUserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, username, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=120, null=False)
    bio = models.TextField(max_length=250, null=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.username

class StatusUser(models.Model):
    CHOICES = [
        ('ONLINE', 'online'),
        ('OFFLINE', 'offline'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=CHOICES)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False

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
    body = models.TextField(max_length=1000, blank=True)
    file = models.FileField(upload_to='chat_files/', null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date_sended = models.DateTimeField(auto_now_add=True)
