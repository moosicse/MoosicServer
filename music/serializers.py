from rest_framework import serializers

from music.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            'id', 'name', 'singer', 'album', 'genres', 'mood',
            'user_group', 'file', 'description',
        )
