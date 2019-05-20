from django.contrib.auth.models import User
from django.db import models

from music.constants import SEX_CHOICES


class Genre(models.Model):
    name = models.CharField(max_length=20)


class Singer(models.Model):
    name = models.CharField(max_length=20)
    gender = models.IntegerField(choices=SEX_CHOICES, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Album(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    singer = models.ManyToManyField(Singer, blank=True, null=True)
    published_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)


class Song(models.Model):
    name = models.CharField(max_length=20)
    singer = models.ForeignKey(Singer, blank=True, null=True, on_delete=models.SET_NULL)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField(Genre, blank=True, null=True, related_name='song_set')
    mood = models.TextField(default='{}')
    user_group = models.ManyToManyField('account.UserProfile', related_name='song_set')
    file = models.FileField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Playlist(models.Model):
    name = models.CharField(max_length=20)
    songs = models.ManyToManyField(Song, related_name='playlist_set')
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
