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





# if __name__ == "__main__":
#     # Get the credentials from environment variables
#     # Get a Spotify authenticated instance
#     sp_instance = authenticate(cid, secret, scope, rur, user)
#
#     list = get_user_followed_artists_list(sp_instance)
#
#     for i in range(0, len(list)):
#         print(list[i])



