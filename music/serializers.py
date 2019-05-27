from rest_framework import serializers

from music.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            'id', 'cover', 'name', 'singer', 'genres',
            'mood', 'user_group', 'description', 'file',
        )
