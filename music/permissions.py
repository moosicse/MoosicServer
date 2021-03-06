from django.contrib.auth.models import AnonymousUser, User
from rest_framework import permissions
from rest_framework.request import Request

from account.services import UserServices
from music.models import Song, Playlist


class UserHasSongPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj: Song):
        if obj.user_group.count() == 0:
            return True

        user = request.user
        if user is None:
            return False
        return UserServices.user_has_access_to_music(user, obj)


class UserHasPlaylistPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request: Request, view, obj: Playlist):
        user = request.user

        if isinstance(user, AnonymousUser):
            return False

        if isinstance(user, User):
            user = user.profile

        return obj.created_by == user
