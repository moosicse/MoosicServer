from django.contrib.auth.models import User
from django.db import models

from music.models import Genre


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    motto = models.TextField(blank=True, null=True)
    prefer_genre = models.ManyToManyField(Genre, related_name='prefer_user_set')


class UserGroup(models.Model):
    name = models.CharField(max_length=20)
    users = models.ManyToManyField(UserProfile, related_name='user_group_set')
