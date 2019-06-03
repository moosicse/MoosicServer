from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import UserProfile


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email',
        )


class AccountSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'id', 'user', 'motto', 'prefer_genre',
        )
