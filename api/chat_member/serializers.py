from rest_framework import serializers

from api.models import ChatMember


class ChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = '__all__'
