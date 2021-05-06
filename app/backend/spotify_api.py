from os import environ
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
from typing import List, Dict
from cid_secr import cid, secret, scope, rur, user


# TODO client
class Spotify():
    # Authenticate to Spotify
    def authenticate(cliend_id: str, client_secret: str, scope: str, rur: str, user: str) -> spotipy.client.Spotify:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=cliend_id,
                client_secret=client_secret,
                scope=scope,
                redirect_uri=rur,
                username=user
            )
        )
        #### Эта штука нужна будет для продления, если что. Потом запихнуть куда надо ####
        util.prompt_for_user_token(username=user,
                                   scope=scope,
                                   client_id=cid,
                                   client_secret=secret,
                                   redirect_uri=rur)

        return sp

    ###   Непосредственно получение списка артистов, на которых подписан данный пользователь
    def get_user_followed_artists_list(sp: spotipy.client.Spotify):
        jason = sp.current_user_followed_artists(limit=20)
        artists_list = []

        for i in range(0, len(jason["artists"]["items"])):
            artists_list.append(jason["artists"]["items"][i]["name"])

        return artists_list

    def get_songname_by_artist_id(sp: spotipy.client.Spotify, id: str):
        jason = sp.artist_top_tracks(artist_id=id)
        songname = jason["tracks"][0]["name"]

        return songname

    def get_artist_id_by_name(sp: spotipy.client.Spotify, name: str):
        jason = sp.search(q=name, type="artist")
        artist_id = jason["artists"]["items"][0]["id"]

        return artist_id




# if __name__ == "__main__":
#     # Get the credentials from environment variables
#     # Get a Spotify authenticated instance
#     sp_instance = authenticate(cid, secret, scope, rur, user)
#
#     list = get_user_followed_artists_list(sp_instance)
#
#     for i in range(0, len(list)):
#         print(list[i])



