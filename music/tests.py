from rest_framework.test import APIClient

from testing.TestCase import TestCases


class TestLuckySong(TestCases):
    def setUp(self):
        self.user1 = self.create_user('user1')
        self.song1 = self.create_song('Song1')
        self.ug1 = self.create_user_group('ug1')
        self.ug1.users.add(self.user1)
        self.song1.user_group.add(self.ug1)

        self.anonymous_client = APIClient(enforce_csrf_checks=True)
        self.user1_client = APIClient(enforce_csrf_checks=True)
        self.user1_client.force_authenticate(user=self.user1)

    def test_anonymous_null_lucky_song(self):
        response_anonymous_lucky = self.anonymous_client.get('/api/song/lucky/')
        self.assertEqual(
            response_anonymous_lucky.json(), {}
        )

    def test_anonymous_lucky_song(self):
        self.song2 = self.create_song('song2')
        for _ in range(5):
            response_anonymous_lucky = self.anonymous_client.get('/api/song/lucky/')
            self.assertEqual(
                response_anonymous_lucky.json()['name'], self.song2.name
            )

    def test_lucky_song(self):

        response_user1 = self.user1_client.get('/api/song/lucky/')
        self.assertEqual(
            response_user1.json()['name'], self.song1.name
        )
