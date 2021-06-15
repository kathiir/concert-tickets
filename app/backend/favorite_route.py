import json
from typing import Dict, Any

from auth_utils import recreate_token_for_response
from const_keys import SUCCESS_KEY, ARTIST_CONCERT_TYPES, DESCRIPTION_KEY, TOKEN_NOT_FOUND, BAN_KEY
from models import User, db, Artist, Concert, concert_simpl_schema, artist_simpl_schema
from utils import check_keys_in_dict


def add_sth_to_favorite(request: Dict[str, Any]) -> Dict[str, Any]:
    args = ['token', 'type', 'id']

    response = {SUCCESS_KEY: True}

    if not check_keys_in_dict(request, args) \
        or not request['type'] in ARTIST_CONCERT_TYPES:
        raise ValueError("incorrect type or keys")

    user = db.session.query(User) \
        .filter(User.user_token == request['token']) \
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if user and user.user_role == 1:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: BAN_KEY}

    if request['type'] == 'artist':
        if artist := db.session.query(Artist).get(int(request['id'])):
            user.favorite_artists.append(artist)
            db.session.commit()
        else:
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    if request['type'] == 'concert':
        if concert := Concert.query.get(int(request['id'])):
            user.favorite_concerts.append(concert)
            db.session.commit()
        else:
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    return recreate_token_for_response(response, request['token'])


def remove_sth_to_favorite(request: Dict[str, Any]) -> Dict[str, Any]:
    args = ['token', 'type', 'id']

    response = {SUCCESS_KEY: True}

    if not check_keys_in_dict(request, args) \
        or not request['type'] in ARTIST_CONCERT_TYPES:
        raise ValueError("incorrect type or keys")

    user = db.session.query(User) \
        .filter(User.user_token == request['token']) \
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if user and user.user_role == 1:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: BAN_KEY}

    if request['type'] == 'artist':
        if artist := db.session.query(Artist).get(int(request['id'])):
            try:
                user.favorite_artists.remove(artist)
                db.session.commit()
            except ValueError:
                pass

        else:
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    if request['type'] == 'concert':
        if concert := Concert.query.get(int(request['id'])):
            try:
                user.favorite_concerts.remove(concert)
                db.session.commit()
            except ValueError:
                pass

        else:
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    return recreate_token_for_response(response, request['token'])


def is_sth_favorite(request: Dict[str, Any]) -> Dict[str, Any]:
    args = ['token', 'type', 'id']

    response = {SUCCESS_KEY: True}

    if not check_keys_in_dict(request, args) \
        or not request['type'] in ARTIST_CONCERT_TYPES:
        raise ValueError("incorrect type or keys")

    user = db.session.query(User) \
        .filter(User.user_token == request['token']) \
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if user and user.user_role == 1:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: BAN_KEY}

    if request['type'] == 'artist':
        if artist := db.session.query(Artist).get(int(request['id'])):
            if artist in user.favorite_artists:
                response['favorite'] = True
            else:
                response['favorite'] = False

    if request['type'] == 'concert':
        if concert := Concert.query.get(int(request['id'])):
            if concert in user.favorite_concerts:
                response['favorite'] = True
            else:
                response['favorite'] = False

    return recreate_token_for_response(response, request['token'])


def get_every_possible_favorites(token: str) -> Dict[str, Any]:
    user = User.query\
        .filter(User.user_token == token)\
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    result = {SUCCESS_KEY: True}

    result['concerts'] = [concert_simpl_schema.dump(x)
                          for x in user.favorite_concerts]

    result['artists'] = [artist_simpl_schema.dump(x)
                         for x in user.favorite_artists]

    return recreate_token_for_response(result, token)



def get_suggested_concerts_by_spotify(token: str) -> Dict[str, Any]:

    user = User.query\
        .filter(User.user_token == token)\
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if not user.user_spotify_token:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'spotify token not found'}

# TODO
