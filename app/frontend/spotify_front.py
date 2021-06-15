from datetime import datetime, timedelta
from pipes import quote
from typing import Any, Dict, Optional

import requests
from flask import request

from cid_secr import cid, secret, rur, scope

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": rur,
    "scope": scope,
    "client_id": cid
}


def get_spotify_auth_url() -> str:
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return auth_url


def pass_response(spotify_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    auth_code = spotify_response['code']

    if 'error' in spotify_response:
        return None

    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": rur,
        'client_id': cid,
        'client_secret': secret,
    }

    token_info_response = requests\
        .post(SPOTIFY_TOKEN_URL, data=payload)\
        .json()

    result = {'spotify_access_token': token_info_response['access_token'],
              'spotify_refresh_token': token_info_response['refresh_token'],
              'spotify_exp_date': (datetime.now() + timedelta(seconds=token_info_response['expires_in'])).isoformat()}

    return result
