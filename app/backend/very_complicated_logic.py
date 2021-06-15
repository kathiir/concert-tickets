from datetime import datetime
from typing import Any, Dict

from genius_api import Genius
from models import ArtistReview, artist_review_schema, concert_review_schema, ConcertReview, User, Artist, Concert, \
    concert_schema, artist_schema
from config import db
from utils import check_keys_in_dict
from auth_utils import recreate_token_for_response
from const_keys import ARTIST_CONCERT_TYPES, SUCCESS_KEY, TOKEN_NOT_FOUND, DESCRIPTION_KEY, BAN_KEY

from sqlalchemy import func, and_


def get_all_reviews(id: int, query_type: str) -> Dict[str, Any]:
    response = {SUCCESS_KEY: True}

    if query_type not in ARTIST_CONCERT_TYPES:
        response[SUCCESS_KEY] = False
        return response

    if query_type == 'artist':
        result = db.session.query(ArtistReview)\
            .filter(ArtistReview.artist_id == id)\
            .all()

        result = [artist_review_schema.dump(x)
                  for x in result]

        response['list'] = result
        return response

    if query_type == 'concert':
        result = db.session.query(ConcertReview)\
            .filter(ConcertReview.concert_id == id)\
            .all()

        result = [concert_review_schema.dump(x)
                  for x in result]

        response['list'] = result
        return response

    response[SUCCESS_KEY] = False
    return response


def add_review_to_artist(request: Dict[str, Any]) -> Dict[str, Any]:
    requested_fields = ['token', 'artist_id',
                        'artist_review_info',
                        'artist_review_rating']

    artist_review_rating = max(0.0, float(request['artist_review_rating']))
    artist_review_rating = min(5.0, artist_review_rating)

    if not check_keys_in_dict(request, requested_fields):
        raise ValueError('Incorrect input data')

    user = db.session.query(User)\
        .filter(User.user_token == request['token'])\
        .first()

    artist = db.session.query(Artist)\
        .filter(Artist.artist_id == int(request['artist_id']))\
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if user and user.user_role == 1:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: BAN_KEY}

    if not artist:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    review = ArtistReview(
        artist_review_info=request['artist_review_info'],
        artist_review_rating=artist_review_rating,
        artist=artist,
        user=user
    )

    db.session.add(review)
    db.session.commit()

    return recreate_token_for_response({SUCCESS_KEY: True}, user.user_token)


def add_review_to_concert(request: Dict[str, Any]) -> Dict[str, Any]:
    requested_fields = ['token', 'concert_id',
                        'concert_review_info',
                        'concert_review_rating']

    if not check_keys_in_dict(request, requested_fields):
        raise ValueError('Incorrect input data')

    user = db.session.query(User)\
        .filter(User.user_token == request['token'])\
        .first()

    concert = db.session.query(Concert)\
        .filter(Concert.concert_id == int(request['concert_id']))\
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if user and user.user_role == 1:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: BAN_KEY}

    if not concert:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    if concert.concert_date > datetime.now():
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not started'}

    if concert.concert_status:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'cancelled'}

    review = ConcertReview(
        concert_review_info=request['concert_review_info'],
        concert_review_rating=float(request['concert_review_rating']),
        concert=concert,
        user=user
    )

    db.session.add(review)
    db.session.commit()

    return recreate_token_for_response({SUCCESS_KEY: True}, user.user_token)


def get_all_info_about_concert(concert_id: int, token: str = "") -> Dict[str, Any]:
    response = dict()

    concert = db.session.query(Concert)\
        .filter(Concert.concert_id == concert_id)\
        .first()

    if not concert:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    concert_average_mark = db.session\
        .query(func.avg(ConcertReview.concert_review_rating))\
        .filter(ConcertReview.concert_id == concert_id)\
        .first()[0]

    concert_is_ended = concert.concert_date <= datetime.now()

    if token and User.query.filter(User.user_token == token).first():
        response['favorite'] = db.session.query(User)\
            .join(User.favorite_concerts)\
            .filter(and_(User.user_token == token, Concert.concert_id == concert_id))\
            .first() is not None

    response[SUCCESS_KEY] = True
    response['concert_average_mark'] = concert_average_mark
    response['concert_is_ended'] = concert_is_ended
    response['concert'] = concert_schema.dump(concert)

    return recreate_token_for_response(response, token)


def get_all_info_about_artist(artist_id: int, token: str = "") -> Dict[str, Any]:
    response = dict()

    artist = db.session.query(Artist)\
        .filter(Artist.artist_id == artist_id)\
        .first()

    if not artist:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not found'}

    artist_average_mark = db.session\
        .query(func.avg(ArtistReview.artist_review_rating))\
        .filter(ArtistReview.artist_id == artist_id)\
        .first()[0]

    if token and User.query.filter(User.user_token == token).first():
        response['favorite'] = db.session.query(User)\
            .join(User.favorite_artists)\
            .filter(and_(User.user_token == token, Artist.artist_id == artist_id))\
            .first() is not None

    if artist.artist_genius_id != 0:
        info = Genius().get_artist_info_by_id(artist.artist_genius_id)
    else:
        info = None

    response[SUCCESS_KEY] = True
    response['info'] = info
    response['artist_average_mark'] = artist_average_mark
    response['artist'] = artist_schema.dump(artist)

    return recreate_token_for_response(response, token)

