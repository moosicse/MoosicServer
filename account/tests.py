from account.services import UserServices
from testing.TestCase import TestCases


class UserGroupTest(TestCases):
    def setUp(self):
        self.user1 = self.create_user('User1')
        self.user2 = self.create_user('User2')
        self.user3 = self.create_user('User3')

        self.user_group1 = self.create_user_group('UG1')
        self.user_group2 = self.create_user_group('UG2')

        self.public_song = self.create_song('Public Song')
        self.ug1_song = self.create_song('UG1 Song')
        self.ug12_song = self.create_song('UG1 2 Song')

        self.user_group1.users.add(self.user1)
        self.user_group2.users.add(self.user1)
        self.user_group2.users.add(self.user2)

        self.ug1_song.user_group.add(self.user_group1)
        self.ug12_song.user_group.add(self.user_group1)
        self.ug12_song.user_group.add(self.user_group2)

    def test_user_profile_has_access_to_music(self):
        for user in [self.user1, self.user2, self.user3]:
            self.assertTrue(UserServices.user_has_access_to_music(
                user, self.public_song
            ))

        self.assertTrue(UserServices.user_has_access_to_music(
            self.user1, self.ug1_song
        ))
        self.assertTrue(UserServices.user_has_access_to_music(
            self.user1, self.ug12_song
        ))

        self.assertFalse(UserServices.user_has_access_to_music(
            self.user2, self.ug1_song
        ))

        self.assertTrue(UserServices.user_has_access_to_music(
            self.user2, self.ug12_song
        ))

        self.assertFalse(UserServices.user_has_access_to_music(
            self.user3, self.ug1_song
        ))

        self.assertFalse(UserServices.user_has_access_to_music(
            self.user3, self.ug12_song
        ))
