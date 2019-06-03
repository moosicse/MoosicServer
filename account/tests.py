from rest_framework.test import APIClient

from account.services import UserServices
from testing.TestCase import TestCases


class UserAccountTest(TestCases):
    def setUp(self):
        self.anonymous_client_1 = APIClient(enforce_csrf_checks=True)
        self.anonymous_client_2 = APIClient(enforce_csrf_checks=False)

        self.user1 = self.create_user('user1')
        self.user1.user.set_password('user1_password')
        self.user1.user.email = 'user1@test.com'
        self.user1.user.save()

    def test_register(self):
        req = self.anonymous_client_1.get('/api/account/profile/')
        self.assertEqual(req.status_code, 403)

        req = self.anonymous_client_1.post(
            '/api/account/',
            data={
                'username': 'test_user1',
                'email': 'test@test.com',
                'password': 'test_pass'
            }
        )
        self.assertNotEqual(req.status_code, 403)

        req = self.anonymous_client_1.get('/api/account/profile/')
        self.assertEqual(req.json()['user']['username'], 'test_user1')

    def test_login_and_logout(self):
        req = self.anonymous_client_2.get('/api/account/profile/')
        self.assertEqual(req.status_code, 403)

        req = self.anonymous_client_2.post(
            '/api/account/login/',
            data={
                'username': self.user1.user.username,
                'password': 'user1_password',
            }
        )
        self.assertNotEqual(req.status_code, 403)

        req = self.anonymous_client_2.get('/api/account/profile/')
        self.assertEqual(req.json()['user']['username'], self.user1.user.username)

        self.anonymous_client_2.post('/api/account/logout/')
        req = self.anonymous_client_2.get('/api/account/profile/')
        self.assertEqual(req.status_code, 403)


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
