from django.contrib import admin

from music.models import Genre, Singer, Album, Song, Playlist


@admin.register(Genre, Singer, Album, Song, Playlist)
class AccountAdmin(admin.ModelAdmin):
    pass

