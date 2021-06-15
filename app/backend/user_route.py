from typing import Any, Dict

from auth_utils import recreate_token_for_response
from models import User, db
from utils import check_keys_in_dict
from const_keys import SUCCESS_KEY, DESCRIPTION_KEY, TOKEN_NOT_FOUND
from validators import url


def change_image(request: Dict[str, Any]) -> Dict[str, Any]:
    approved_args = ['token', 'user_photo']

    if not check_keys_in_dict(request, approved_args):
        raise ValueError("incorrect keys")

    if not url(request['user_photo']):
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'incorrect img url'}

    user = User.query\
        .filter(User.user_token == request['token'])\
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    user.user_photo = request['user_photo']
    db.session.commit()
    return recreate_token_for_response({SUCCESS_KEY: True},
                                       request['token'])


def change_additional_user_token(request: Dict[str, Any]) -> Dict[str, Any]:

    if not 'token' in request and \
        not ('gcalendar_token' in request or
         'spotify_token' in request):
        raise ValueError("incorrect keys")

    user = User.query\
        .filter(User.user_token == request['token'])\
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if 'gcalendar_token' in request:
        if not request['gcalendar_token']:
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'incorrect additional token'}

        user.user_gcalendar_token = request['gcalendar_token']

    if 'spotify_token' in request:
        if not request['spotify_token']:
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'incorrect additional token'}

        user.user_spotify_token = request['spotify_token']

    db.session.commit()
    return recreate_token_for_response({SUCCESS_KEY: True},
                                       request['token'])