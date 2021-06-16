from base64 import b64encode
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from auth_utils import recreate_token_for_response
from cid_secr import cid, secret
from const_keys import SUCCESS_KEY, DESCRIPTION_KEY, TOKEN_NOT_FOUND
from models import User, db, Artist, concert_simpl_schema

authorization_header = 'Basic ' + b64encode(f"{cid}:{secret}".encode()).decode()
grant_type = 'user-follow-read'


def request_for_token(user: User) -> Optional[str]: # returns access token
    if user.user_spotify_token_exp_date < datetime.now():
        return user.user_spotify_access_token

    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': authorization_header}
    body = {'grant_type': 'refresh_token',
            'refresh_token': user.user_spotify_refresh_token}

    response = requests.post(url,
                             data=urlencode(body),
                             headers=headers).json()

    if 'error' in response:
        return None

    if 'refresh_token' in response:
        user.user_spotify_refresh_token = response['refresh_token']

    user.user_spotify_access_token = response['access_token']
    user.user_spotify_token_exp_date = datetime.now() + timedelta(seconds=response['expires_in'])

    db.session.add(user)
    db.session.commit()

    return response['access_token']


def get_concert_for_users_followed_artists(token: str) -> Dict[str, Any]:
    user = User.query\
        .filter(User.user_token == token)\
        .first()

    if not user:
        return {SUCCESS_KEY: False,
                DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if not user.user_spotify_access_token:
        return {SUCCESS_KEY: False,
                DESCRIPTION_KEY: 'spotify token not found'}

    access_token = request_for_token(user)

    if not access_token:
        return {SUCCESS_KEY: False,
                DESCRIPTION_KEY: 'no spotify response'}

    url = 'https://api.spotify.com/v1/me/following?type=artist&limit=10'
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    spotify_response = requests\
        .get(url, headers=headers)

    spotify_response = spotify_response.json()

    response = {SUCCESS_KEY: True}

    concerts = list()

    for item in spotify_response['artists']['items']:
        artist = Artist.query\
            .filter(Artist.artist_spotify_id == item['id'])\
            .first()

        concerts.extend([concert_simpl_schema.dump(x)
                         for x in artist.performances])

    response['concerts'] = concerts
    return recreate_token_for_response(response, token)
