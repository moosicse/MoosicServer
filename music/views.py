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
        all_song = Song.objects.all()
        selected = random.sample(range(all_song.count()), 1)[0]
        return Response(SongSerializer(all_song[selected]).data)
