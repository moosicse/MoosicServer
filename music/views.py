from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from account.services import UserServices
from music.models import Song
from music.permissions import UserHasSongPermission
from music.serializers import SongSerializer

import random


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (UserHasSongPermission,)

    @action(detail=False)
    def lucky(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            songs_to_select = Song.objects.filter(user_group__isnull=True)
        else:
            songs_to_select = Song.objects.filter(user_group__users=user)

        if songs_to_select.count() == 0:
            return Response({})

        selected = random.sample(range(songs_to_select.count()), 1)[0]
        return Response(SongSerializer(songs_to_select[selected]).data)
