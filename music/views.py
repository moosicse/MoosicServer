from typing import Any

from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from account.services import UserServices
from music.constants import MOOD_SONG_COUNT
from music.models import Song, Playlist, Album, Singer
from music.permissions import UserHasSongPermission, UserHasPlaylistPermission
from music.serializers import SongSerializer, PlaylistSerializer, AlbumSerializer, SingerSerializer

import random

from music.services import MusicService


class AlbumViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = ()

    @action(detail=True)
    def songs(self, request: Request, pk: int):
        album = Album.objects.get(id=pk)
        songs = []
        for song in album.song_set.all():
            if UserServices.user_has_access_to_music(request.user, song):
                songs.append(song)
        return Response(SongSerializer(songs, many=True).data)


class SingerViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    permission_classes = ()

    @action(detail=True)
    def songs(self, request: Request, pk: int):
        singer = Singer.objects.get(id=pk)
        songs = []
        for song in singer.song_set.all():
            if UserServices.user_has_access_to_music(request.user, song):
                songs.append(song)
        return Response(SongSerializer(songs, many=True).data)


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
    mixins.RetrieveModelMixin,
):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (UserHasPlaylistPermission,)

    def create(self, request: Request, *args: Any, **kwargs: Any):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response(status=403)
        if isinstance(user, User):
            user = user.profile
        name = request.data.get('name', None)
        if not name:
            return Response(status=403)
        playlist = Playlist.objects.create(
            name=name, created_by=user
        )
        return Response(PlaylistSerializer(playlist).data)

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
        if isinstance(user, User):
            user = user.profile

        playlist = Playlist.objects.filter(id=pk).first()
        if not playlist or playlist.created_by != user:
            return Response(status=403)
        # Have to use POST
        song: str = request.data.get('song', None)
        res: list = []

        if song:
            try:
                song = int(song)
            except:
                return Response(status=403)
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
        if isinstance(user, User):
            user = user.profile

        playlist = Playlist.objects.filter(id=pk).first()
        if not playlist or playlist.created_by != user:
            return Response(status=403)

        song: str = request.data.get('song', None)
        res: list = []
        if song:
            try:
                song = int(song)
            except:
                return Response(status=403)
            song_instance = Song.objects.filter(id=song).first()
            if song_instance:
                playlist.songs.remove(song_instance)
                res.append(song)
        return Response(res)

    @action(detail=False)
    def motion(self, request: Request):
        motion = request.query_params.get('motion', '')
        query = Q(mood='mood')
        if motion == 'joy':
            query |= Q(mood='Happy')
            query |= Q(mood='Excited')
        elif motion == 'sadness':
            query |= Q(mood='Sad')
            query |= Q(mood='Calm')
        elif motion == 'anger':
            query |= Q(mood='Calm')
        elif motion == 'surprise':
            query |= Q(mood='Excited')

        songs = Song.objects.filter(query)
        import logging
        logging.warning(query)
        if len(songs) > MOOD_SONG_COUNT:
            songs = random.sample(list(songs), MOOD_SONG_COUNT)
        return Response(SongSerializer(songs, many=True).data)
