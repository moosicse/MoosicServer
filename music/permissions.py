from rest_framework import permissions

from account.services import UserServices
from music.models import Song


class UserHasSongPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj: Song):
        if obj.user_group.count() == 0:
            return True

        user = request.user
        if user is None:
            return False
        return UserServices.user_has_access_to_music(user.profile, obj)
