from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase

from account.models import UserProfile, UserGroup
from music.models import Song, Playlist


class TestCases(DjangoTestCase):

    # Model account
    @classmethod
    def get_password(cls, username: str):
        return username + 'test_case_password'

    def _create_user(
            self, username: str,
            email: str = None,
            is_staff: bool = False,
            is_superuser: bool = False,
    ):
        if email is None:
            email = '%s@%s.com' % (username, username)
        user = User.objects.create(
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            email=email)
        user.set_password(self.get_password(username))
        user.save()

        return user

    def create_user(self, *args, **kwargs):
        user = self._create_user(*args, **kwargs)
        user_profile = UserProfile.objects.create(
            user=user,
        )
        return user_profile

    def create_user_group(self, name: str):
        user_group = UserGroup.objects.create(name=name)
        return user_group

    # Model music
    def create_song(self, name: str):
        return Song.objects.create(name=name)

    def create_playlist(self, name: str):
        return Playlist.objects.create(name=name)
