from django.db.models import Q

from music.models import Song


class MusicService:
    @classmethod
    def search_song_by_query(cls, query):
        q = Q(name__icontains=query) | Q(singer__name__icontains=query)
        return Song.objects.filter(q)
