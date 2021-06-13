import unittest
import requests
from parameterized import parameterized
from tests.test_consts import *
import genius_api
import spotify_api

res_response = requests.get(app_url)
spotify_str = ""
genius = genius_api.Genius()
spotify = spotify_api.Spotify()


class RestTest(unittest.TestCase):
    def test_check_status_code(self):
        self.assertEqual(res_response.status_code, 200)

    def test_check_content_type(self):
        self.assertEqual(res_response.headers['Content-Type'], "text/html; charset=utf-8")


class ParametrizedRestTest(unittest.TestCase):
    @parameterized.expand(test_parameterized_data_concerts)
    def test_check_response_body_concert(self, concert_id, concert_name):
        response = requests.get(f"{app_url}concert/{concert_id}")
        response_body = response.text
        self.assertTrue(concert_name in response_body)

    @parameterized.expand(test_parameterized_data_artists)
    def test_check_response_body_concert(self, artist_id, artist_name):
        response = requests.get(f"{app_url}artists/{artist_id}")
        response_body = response.text
        self.assertTrue(artist_name in response_body)


class GeniusTest(unittest.TestCase):
    def test_get_artist_info_by_id(self):
        self.assertEqual(genius.get_artist_info_by_id(13).__len__(), 1)

    def test_get_artist_id_by_songname(self):
        self.assertEqual(genius.get_artist_id_by_songname(test_songname), test_songname_res)


class SpotifyTest(unittest.TestCase):
    def test_get_artist_id_by_name(self):
        global spotify_str
        spotify_str = spotify.get_artist_id_by_name(test_1_res)
        self.assertEqual(spotify_str, test_1_spotipy_id)

    def test_get_artist_name_by_id(self):
        self.assertEqual(spotify.get_artist_name_by_id(test_1_spotipy_id), test_1_res)

    def test_get_artist_name_by_id_is_equal(self):
        self.assertEqual(spotify.get_artist_name_by_id(spotify_str), test_1_res)

    def test_get_songname_by_artist_id(self):
        self.assertEqual(spotify.get_artist_name_by_id(test_2_spotipy_id), test_2_res)


if __name__ == '__main__':
    unittest.main()
