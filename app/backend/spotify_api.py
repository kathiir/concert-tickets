import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

from cid_secr import cid, secret


# TODO client
class Spotify:
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def authenticate(self, cliend_id: str, client_secret: str, scope: str, rur: str,
                     user: str) -> spotipy.client.Spotify:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=cliend_id,
                client_secret=client_secret,
                scope=scope,
                redirect_uri=rur,
                username=user
            )
        )
        util.prompt_for_user_token(username=user,
                                   scope=scope,
                                   client_id=cid,
                                   client_secret=secret,
                                   redirect_uri=rur)

        return sp

    #То же самое, что и первое, но без зависимости от авторизованности пользователя
    def authenticate_unauthorized(cliend_id: str, client_secret: str, scope: str, rur: str) -> spotipy.client.Spotify:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=cliend_id,
                client_secret=client_secret,
                scope=scope,
                redirect_uri=rur
            )
        )
        #### Эта штука нужна будет для продления, если что. Потом запихнуть куда надо ####
        util.prompt_for_user_token(scope=scope,
                                   client_id=cid,
                                   client_secret=secret,
                                   redirect_uri=rur)

        return sp


    def get_user_followed_artists_list(self, sp: spotipy.client.Spotify):
        jason = sp.current_user_followed_artists(limit=20)
        artists_list = []

        for i in range(0, len(jason["artists"]["items"])):
            artists_list.append(jason["artists"]["items"][i]["name"])

        return artists_list

    def get_songname_by_artist_id(self, id: str):
        jason = self.sp.artist_top_tracks(artist_id=id)
        songname = jason["tracks"][0]["name"]
        return songname

    def get_artist_name_by_id(self, id: str):
        jason = self.sp.artist(artist_id=id)
        return jason["name"]

    def get_artist_image_by_id(self, id: str):
        jason = self.sp.artist(artist_id=id)
        return jason["images"][0]['url']

    def get_artist_id_by_name(self, name: str):
        jason = self.sp.search(q=name, type="artist")
        try:
            artist_id = jason["artists"]["items"][0]["id"]
            return artist_id
        except IndexError:
            return 0



