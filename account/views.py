from typing import Any

from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from account.models import UserProfile
from account.serializers import AccountSerializer
from account.services import AccountServices


class AccountViewSet(
    viewsets.ViewSet,
    mixins.CreateModelMixin,
):
    # queryset = UserProfile.objects.all()
    # serializer_class = AccountSerializers
    permission_classes = ()

    def create(self, request: Request, *args: Any, **kwargs: Any):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not username or not password or not email:
            return Response(status=403)

        user = User.objects.create_user(username, email, password)
        user_profile = UserProfile.objects.create(
            user=user
        )

        django_login(request, user)
        return Response(AccountSerializer(user_profile).data)

    @action(detail=False)
    def profile(self, request):
        user = request.user
        if user.is_authenticated:
            return Response(AccountSerializer(user.profile).data)
        return Response(status=403)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        username = request.data['username']
        password = request.data['password']

        user_profile = AccountServices.get_user_by_email_or_name(username)
        if not user_profile:
            return Response({'error': 'Your username or password is not correct.'}, status=401)

        username = user_profile.user.username
        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Your username or password is not correct.'}, status=401)

        django_login(request, user)
        return Response(AccountSerializer(user.profile).data)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        django_logout(request)
        return Response({})
