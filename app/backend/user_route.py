from typing import Any, Dict

from validators import url

from auth_utils import recreate_token_for_response
from const_keys import SUCCESS_KEY, DESCRIPTION_KEY, TOKEN_NOT_FOUND
from models import User, db
from utils import check_keys_in_dict


def change_image(request: Dict[str, Any]) -> Dict[str, Any]:
    approved_args = ['token', 'user_photo']

    if not check_keys_in_dict(request, approved_args):
        raise ValueError("incorrect keys")

    if not url(request['user_photo']):
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'incorrect img url'}

    user = User.query \
        .filter(User.user_token == request['token']) \
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    user.user_photo = request['user_photo']
    db.session.commit()
    return recreate_token_for_response({SUCCESS_KEY: True},
                                       request['token'])


def change_additional_user_token(request: Dict[str, Any]) -> Dict[str, Any]:
    google_request_keys = ['google_access_token',
                           'google_refresh_token']

    spotify_request_keys = ['spotify_access_token',
                            'spotify_refresh_token',
                            'spotify_token_exp_date']

    if not 'token' in request and \
            (not all(google_key in request
                     for google_key in google_request_keys) or
             not all(spotify_key in request
                     for spotify_key in spotify_request_keys)):
        raise ValueError("incorrect keys")

    user = User.query \
        .filter(User.user_token == request['token']) \
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if 'google_access_token' in request:
        if not request['google_access_token']:
            return {SUCCESS_KEY: False,
                    DESCRIPTION_KEY: 'incorrect google token'}

        user.user_google_access_token = request['google_access_token']
        user.user_google_refresh_token = request['google_refresh_token']

    if 'spotify_access_token' in request:
        if not request['spotify_access_token']:
            return {SUCCESS_KEY: False,
                    DESCRIPTION_KEY: 'incorrect spotify token'}

        user.user_spotify_access_token = request['spotify_access_token']
        user.user_spotify_refresh_token = request['spotify_refresh_token']
        user.user_spotify_token_exp_date = request['spotify_exp_date']

    db.session.commit()

    return recreate_token_for_response({SUCCESS_KEY: True},
                                       request['token'])


def remove_additional_tokens(request: Dict[str, Any]) -> Dict[str, Any]:
    approved_args = ['type', 'token']

    if not check_keys_in_dict(request, approved_args):
        raise ValueError("incorrect keys")

    user = User.query\
        .filter(User.user_token == request['token'])\
        .first()

    if not user:
        raise ValueError(TOKEN_NOT_FOUND)

    if request['type'] == 'google':
        user.user_google_access_token = None
        user.user_google_refresh_token = None
        db.session.commit()
        return recreate_token_for_response({SUCCESS_KEY: True},
                                           request['token'])

    if request['type'] == 'spotify':
        user.user_spotify_access_token = None
        user.user_spotify_refresh_token = None
        user.user_spotify_token_exp_date = None
        db.session.commit()
        return recreate_token_for_response({SUCCESS_KEY: True},
                                           request['token'])

    raise ValueError("incorrect type")
