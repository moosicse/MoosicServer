from rest_framework.test import APIClient

from testing.TestCase import TestCases


class TestAlbumViewSet(TestCases):
    def setUp(self):
        self.anonymous_client = APIClient(enforce_csrf_checks=True)

        self.user1 = self.create_user('user1')
        self.user1_client = APIClient(enforce_csrf_checks=True)
        self.user1_client.force_authenticate(user=self.user1)

        self.song1 = self.create_song('song1')
        self.song2 = self.create_song('song2')
        self.song3 = self.create_song('song3')

        self.ug1 = self.create_user_group('ug1')
        self.ug1.users.add(self.user1)
        self.song1.user_group.add(self.ug1)

        self.album1 = self.create_album('album1')

        self.song1.album = self.album1
        self.song1.save()
        self.song2.album = self.album1
        self.song2.save()
        self.song3.album = self.album1
        self.song3.save()

    def test_anonymous_album_api(self):
        req = self.anonymous_client.get('/api/album/%d/' % self.album1.id)
        self.assertEqual(req.json()['name'], self.album1.name)

        req = self.anonymous_client.get('/api/album/%d/songs/' % self.album1.id)
        self.assertEqual(len(req.json()), 2)

    def test_user1_album_api(self):
        req = self.user1_client.get('/api/album/%d/' % self.album1.id)
        self.assertEqual(req.json()['name'], self.album1.name)

        req = self.user1_client.get('/api/album/%d/songs/' % self.album1.id)
        self.assertEqual(len(req.json()), 3)


class TestSingerViewSet(TestCases):
    def setUp(self):
        self.anonymous_client = APIClient(enforce_csrf_checks=True)

        self.user1 = self.create_user('user1')
        self.user1_client = APIClient(enforce_csrf_checks=True)
        self.user1_client.force_authenticate(user=self.user1)

        self.song1 = self.create_song('song1')
        self.song2 = self.create_song('song2')
        self.song3 = self.create_song('song3')

        self.ug1 = self.create_user_group('ug1')
        self.ug1.users.add(self.user1)
        self.song1.user_group.add(self.ug1)

        self.singer1 = self.create_singer('singer1')

        self.song1.singer = self.singer1
        self.song1.save()
        self.song2.singer = self.singer1
        self.song2.save()
        self.song3.singer = self.singer1
        self.song3.save()

    def test_anonymous_album_api(self):
        req = self.anonymous_client.get('/api/singer/%d/' % self.singer1.id)
        self.assertEqual(req.json()['name'], self.singer1.name)

        req = self.anonymous_client.get('/api/singer/%d/songs/' % self.singer1.id)
        self.assertEqual(len(req.json()), 2)

    def test_user1_singer_api(self):
        req = self.user1_client.get('/api/singer/%d/' % self.singer1.id)
        self.assertEqual(req.json()['name'], self.singer1.name)

        req = self.user1_client.get('/api/singer/%d/songs/' % self.singer1.id)
        self.assertEqual(len(req.json()), 3)


class TestSongSearchViewSet(TestCases):
    def setUp(self):
        self.anonymous_client = APIClient(enforce_csrf_checks=True)

        self.user1 = self.create_user('user1')
        self.user1_client = APIClient(enforce_csrf_checks=True)
        self.user1_client.force_authenticate(user=self.user1)

        self.song1 = self.create_song('song1')
        self.song2 = self.create_song('song2')
        self.song3 = self.create_song('song3')

        self.ug1 = self.create_user_group('ug1')
        self.ug1.users.add(self.user1)
        self.song1.user_group.add(self.ug1)

        self.singer1 = self.create_singer('singer1')
        self.song2.singer = self.singer1
        self.song2.save()

    def test_query_singer(self):
        req = self.anonymous_client.get('/api/song/search/', {'query': 'singer1'})
        self.assertEqual(len(req.json()), 1)

    def test_query_permission(self):
        req = self.anonymous_client.get('/api/song/search/', {'query': 'song'})
        self.assertEqual(len(req.json()), 2)

        req = self.user1_client.get('/api/song/search/', {'query': 'song'})
        self.assertEqual(len(req.json()), 3)


class TestPlaylistViewSet(TestCases):
    def setUp(self):
        self.anonymous_client = APIClient(enforce_csrf_checks=True)

        self.user1 = self.create_user('user1')
        self.user1_client = APIClient(enforce_csrf_checks=True)
        self.user1_client.force_authenticate(user=self.user1)

        self.user2 = self.create_user('user2')
        self.user2_client = APIClient(enforce_csrf_checks=True)
        self.user2_client.force_authenticate(user=self.user2)

        self.song1 = self.create_song('Song1')
        self.song2 = self.create_song('Song2')
        self.song3 = self.create_song('Song3')

        self.playlist1 = self.create_playlist('user1_playlist')
        self.playlist1.created_by = self.user1
        self.playlist1.save()
        self.playlist2 = self.create_playlist('user2_playlist')
        self.playlist2.created_by = self.user2
        self.playlist2.save()

    def test_create_and_remove_playlist(self):
        req = self.user1_client.post('/api/playlist/', data={'name': 'user1_playlist'})
        self.assertEqual(req.json()['name'], 'user1_playlist')
        playlist_id = req.json()['id']
        req = self.user1_client.get('/api/playlist/')
        self.assertEqual(len(req.json()), 2)
        self.user1_client.delete('/api/playlist/%d/' % playlist_id)
        req = self.user1_client.get('/api/playlist/')
        self.assertEqual(len(req.json()), 1)

        req = self.user2_client.post('/api/playlist/', data={'name': 'user2_playlist'})
        self.assertEqual(req.json()['name'], 'user2_playlist')
        playlist_id = req.json()['id']
        req = self.user2_client.get('/api/playlist/')
        self.assertEqual(len(req.json()), 2)
        self.user2_client.delete('/api/playlist/%d/' % playlist_id)
        req = self.user2_client.get('/api/playlist/')
        self.assertEqual(len(req.json()), 1)

        anonymous_req = self.anonymous_client.post('/api/playlist/', data={'name': 'anonymous_playlist'})
        self.assertEqual(anonymous_req.status_code, 403)

        anonymous_req = self.anonymous_client.delete('/api/playlist/%d/' % playlist_id)
        self.assertEqual(anonymous_req.status_code, 404)

    def test_add_song_to_playlist(self):
        req = self.user1_client.post(
            '/api/playlist/%d/add_song/' % self.playlist1.id,
            data={'song': [self.song1.id, self.song2.id]}
        )
        self.assertEqual(len(req.json()), 2)
        req = self.user2_client.post(
            '/api/playlist/%d/add_song/' % self.playlist2.id,
            data={'song': [self.song1.id, self.song2.id, self.song3.id]}
        )
        self.assertEqual(len(req.json()), 3)

        req = self.user1_client.post(
            '/api/playlist/%d/add_song/' % self.playlist2.id,
            data={'song': [self.song1.id]}
        )
        self.assertEqual(req.status_code, 403)

    def test_anonymous(self):
        req = self.anonymous_client.post(
            '/api/playlist/%d/add_song/' % self.playlist2.id,
            data={'song': [self.song1.id]}
        )
        self.assertEqual(req.status_code, 403)

    def test_remove_song_to_playlist(self):
        req = self.user1_client.post(
            '/api/playlist/%d/remove_song/' % self.playlist1.id,
            data={'song': [self.song2.id]}
        )
        self.assertEqual(len(req.json()), 1)
        req = self.user1_client.get('/api/playlist/')
        self.assertEqual(len(req.json()), 1)


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
                response_anonymous_lucky.json()[0]['name'], self.song2.name
            )

    def test_lucky_song(self):

        response_user1 = self.user1_client.get('/api/song/lucky/')
        self.assertEqual(
            response_user1.json()[0]['name'], self.song1.name
        )
