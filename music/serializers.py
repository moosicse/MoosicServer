from rest_framework import serializers

from music.models import Song, Playlist


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            'id', 'cover', 'name', 'singer', 'genres',
            'mood', 'user_group', 'description', 'file',
        )


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Playlist
        fields = (
            'id', 'name', 'songs', 'created_by',
        )
