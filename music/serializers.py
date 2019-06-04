from rest_framework import serializers

from music.models import Song, Playlist, Album, Singer


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = (
            'id', 'name', 'gender', 'birthday', 'country', 'description',
        )


class AlbumSerializer(serializers.ModelSerializer):
    singer = SingerSerializer()

    class Meta:
        model = Album
        fields = (
            'id', 'name', 'cover', 'singer', 'published_date', 'description',
        )


class SongSerializer(serializers.ModelSerializer):
    singer = SingerSerializer()
    album = AlbumSerializer()

    class Meta:
        model = Song
        fields = (
            'id', 'cover', 'name', 'singer', 'album', 'genres',
            'mood', 'user_group', 'description', 'file',
        )


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Playlist
        fields = (
            'id', 'name', 'songs', 'created_by',
        )
