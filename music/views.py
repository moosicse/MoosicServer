from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

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

        query = Q(user_group__isnull=True)
        if not isinstance(user, AnonymousUser):
            query |= Q(user_group__users=user.id)
        songs_to_select = Song.objects.filter(query)

        if songs_to_select.count() == 0:
            return Response({})

        selected = random.sample(range(songs_to_select.count()), 1)[0]
        return Response(SongSerializer(songs_to_select[selected]).data)
