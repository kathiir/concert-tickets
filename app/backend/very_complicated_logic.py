from typing import Dict, Any

from models import ArtistReview, artist_review_schema, concert_review_schema, ConcertReview, User, Artist, Concert
from config import db
from utils import check_keys_in_dict
from auth_utils import recreate_token_for_response


def get_all_reviews(request: Dict[str, Any]) -> Dict[str, Any]:
    response = {'success': True}

    if not check_keys_in_dict(request, ['id', 'type']) \
            or int(request['id']) < 1 \
            or request['type'] not in ['artist', 'concert']:

        response['success'] = False
        return response

    if request['type'] == 'artist':
        result = db.session.query(ArtistReview)\
            .filter(ArtistReview.artist_id == int(request['id']))\
            .all()

        result = [artist_review_schema.dump(x)
                  for x in result]

        response['list'] = result
        return response

    if request['type'] == 'concert':
        result = db.session.query(ConcertReview)\
            .filter(ConcertReview.concert_id == int(request['id']))\
            .all()

        result = [concert_review_schema.dump(x)
                  for x in result]

        response['list'] = result
        return response

    response['success'] = False
    return response


def add_review_to_artist(request: Dict[str, Any]) -> Dict[str, Any]:
    requested_fields = ['token', 'artist_id',
                        'artist_review_info',
                        'artist_review_rating']

    if not check_keys_in_dict(request, requested_fields):
        raise ValueError('Incorrect input data')

    user = db.session.query(User)\
        .filter(User.user_token == request['token'])\
        .first()

    artist = db.session.query(Artist)\
        .filter(Artist.artist_id == int(request['artist_id']))\
        .first()

    if not user or user.user_role == 1:
        return {'success': False, 'description': 'authorization'}

    if not artist:
        return {'success': False, 'description': 'not found'}

    review = ArtistReview(
        artist_review_info=request['artist_review_info'],
        artist_review_rating=float(request['artist_review_rating']),
        artist=artist,
        user=user
    )

    db.session.add(review)
    db.session.commit()

    return recreate_token_for_response({'success': True}, user.user_token)


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

    if not user or user.user_role == 1:
        return {'success': False, 'description': 'authorization'}

    if not concert:
        return {'success': False, 'description': 'not found'}

    if concert.concert_status:
        return {'success': False, 'description': 'cancelled'}

    review = ConcertReview(
        concert_review_info=request['concert_review_info'],
        concert_review_rating=float(request['concert_review_rating']),
        concert=concert,
        user=user
    )

    db.session.add(review)
    db.session.commit()

    return recreate_token_for_response({'success': True}, user.user_token)
