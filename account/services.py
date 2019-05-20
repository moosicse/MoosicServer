from django.contrib.auth.models import User

from account.models import UserProfile
from music.models import Song


class UserServices:
    @classmethod
    def _user_has_access_to_music(cls, user: User, song: Song):
        user_profile = user.profile
        return cls.user_has_access_to_music(user_profile, song)

    @classmethod
    def user_has_access_to_music(cls, user_profile: UserProfile, song: Song):
        user_groups = song.user_group.all()
        if user_groups.count() == 0:
            # If a song has no user group, it's public.
            return True
        for user_group in user_groups:
            if user_profile in user_group.users.all():
                return True
        return False
