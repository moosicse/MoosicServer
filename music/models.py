from django.contrib.auth.models import User
from django.db import models

from music.constants import SEX_CHOICES


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Singer(models.Model):
    name = models.CharField(max_length=20)
    gender = models.IntegerField(choices=SEX_CHOICES, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    cover = models.ImageField(upload_to='image', blank=True, null=True)
    singer = models.ManyToManyField(Singer)
    published_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=20)
    cover = models.ImageField(upload_to='image', blank=True, null=True)
    singer = models.ForeignKey(Singer, blank=True, null=True, on_delete=models.SET_NULL)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField(Genre, blank=True, related_name='song_set')
    mood = models.TextField(default='{}')
    user_group = models.ManyToManyField('account.UserGroup', blank=True, related_name='song_set')
    file = models.FileField(upload_to='music', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=20)
    songs = models.ManyToManyField(Song, related_name='playlist_set')
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
