from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from music.models import Song, Playlist
from music.permissions import UserHasSongPermission, UserHasPlaylistPermission
from music.serializers import SongSerializer, PlaylistSerializer

import random

from music.services import MusicService


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
        return Response(SongSerializer([songs_to_select[selected]], many=True).data)

    @action(detail=False)
    def search(self, request: Request):
        query = request.query_params.get('query', None)
        if not query:
            return Response([])
        search_result = MusicService.search_song_by_query(query)
        res = []
        for item in search_result:
            try:
                self.check_object_permissions(request, item)
                res.append(item)
            except Exception:
                pass
        return Response(SongSerializer(res, many=True).data)


class PlaylistViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (UserHasPlaylistPermission,)

    def create(self, request: Request, *args: Any, **kwargs: Any):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response(status=403)
        name = request.data.get('name', None)
        if not name:
            return Response(status=403)
        playlist = Playlist.objects.create(
            name=name, created_by=user
        )
        return Response(PlaylistSerializer(playlist).data)

    def destroy(self, request: Request, *args: Any, **kwargs: Any):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response(status=403)
        playlist = self.get_object()
        if playlist:
            playlist.delete()
        return Response({})

    def list(self, request: Request, *args: Any, **kwargs: Any):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response(status=403)

        playlist = Playlist.objects.filter(created_by=user.id)
        return Response(PlaylistSerializer(playlist, many=True).data)

    @action(detail=True, methods=['POST'])
    def add_song(self, request: Request, pk: int):
        user = request.user

        if isinstance(user, AnonymousUser):
            return Response(status=403)

        playlist = Playlist.objects.filter(id=pk).first()
        if not playlist or playlist.created_by != user:
            return Response(status=403)
        # Have to use POST
        songs: list = request.POST.getlist('song', [])
        res: list = []
        for song in songs:
            song_instance = Song.objects.filter(id=song).first()
            if song_instance:
                playlist.songs.add(song_instance)
                res.append(song)
        return Response(res)

    @action(detail=True, methods=['POST'])
    def remove_song(self, request: Request, pk: int):
        user = request.user

        if isinstance(user, AnonymousUser):
            return Response(status=403)

        playlist = Playlist.objects.filter(id=pk).first()
        if not playlist or playlist.created_by != user:
            return Response(status=403)
        songs: list = request.data.get('song')
        res: list = []
        for song in songs:
            song_instance = Song.objects.filter(id=song).first()
            if song_instance:
                playlist.songs.remove(song_instance)
                res.append(song)
        return Response(res)
