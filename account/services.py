from django.contrib.auth.models import User
from django.db.models import Q

from account.models import UserProfile
from music.models import Song


class UserServices:

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


class AccountServices:
    @classmethod
    def get_user_by_email_or_name(cls, email_or_name):
        return UserProfile.objects.filter(
            Q(user__username=email_or_name) | Q(user__email=email_or_name)
        ).first()
