import json

from flask import Flask, request, make_response, jsonify, abort
import os

from config import app
from genius_api import Genius
from spotify_api import Spotify

from auth_utils import register_user_with_response, login_user_by_login_and_pass, recreate_user_token

from very_complicated_logic import *

from utils import simplify_json_result

genius = Genius()
spotify = Spotify()


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# nickname, email, password, password_check
@app.route('/registration', methods=['POST'])
def register_user():
    data = simplify_json_result(request.get_json())
    response = register_user_with_response(data)
    return json.dumps(response), 200, {'ContentType': 'application/json'}


# login(email or login), password
@app.route('/login', methods=['POST'])
def login_user():
    data = simplify_json_result(
        request.get_json())  # костыль, так как надо сделать так, чтобы фронт не кидал списки вида: {'login': ['login']}
    response = login_user_by_login_and_pass(data['login'], data['password'])
    return json.dumps(response), 200, {'ContentType': 'application/json'}


@app.route('/user_short_info', methods=['POST'])
def user_short_info():
    data = simplify_json_result(request.get_json())
    response = {'success': True}

    if not 'token' in data:
        response = {'success': False}
        return json.dumps(response), 400, {'ContentType': 'application/json'}

    token = recreate_user_token(data['token'])
    if not token:  # empty
        response['success'] = False
    else:
        response['user'] = user_simpl_schema.dump(db.session \
                                                  .query(User) \
                                                  .filter(User.user_token == token) \
                                                  .first())

        if data['token'] != token:
            response['token'] = token

    return json.dumps(response), 200, {'ContentType': 'application/json'}


# token
# returns: token (if expired), user, success (false if need to login)
@app.route('/user_profile', methods=['POST'])
def user_profile():
    data = simplify_json_result(request.get_json())
    response = {'success': True}

    if not 'token' in data:
        response = {'success': False}
        return json.dumps(response), 400, {'ContentType': 'application/json'}

    token = recreate_user_token(data['token'])
    if not token:  # empty
        response['success'] = False
    else:
        response['user'] = user_schema.dump(db.session \
                                            .query(User) \
                                            .filter(User.user_token == token) \
                                            .first())

        if data['token'] != token:
            response['token'] = token

    return json.dumps(response), 200, {'ContentType': 'application/json'}


# id, type (artist, concert): лучше enum, но пофиг
# return list<review>
@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    data = simplify_json_result(request.get_json())
    response = get_all_reviews(data)

    if not response['success']:
        return json.dumps(response), 400, {'ContentType': 'application/json'}

    return json.dumps(response), 200, {'ContentType': 'application/json'}


@app.route('/add_artist_review', methods=['POST'])
def add_artist_review():
    data = simplify_json_result(request.get_json())
    try:
        response = add_review_to_artist(data)
        return json.dumps(response), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

@app.route('/artist/s/<string:artist_name>', methods=['GET'])
def get_artist_search(artist_name):
    result = Artist.query.filter(Artist.artist_name.ilike(f'%{artist_name}%'))
    if result is None:
        return jsonify(concerts=[])
    return jsonify(artists=[artist_simpl_schema.dump(i) for i in result])


@app.route('/artist/<int:artist_id>', methods=['GET'])
def get_artist_by_id(artist_id):
    result = Artist.query.get(artist_id)
    if result is None:
        abort(404)
    if result.artist_genius_id != 0:
        info = genius.get_artist_info_by_id(result.artist_genius_id)
    else:
        info = None
    return jsonify(artist=artist_schema.dump(result), info=info)


@app.route('/concerts', methods=['GET'])
def get_concert_list():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    result = Concert.query.order_by(Concert.concert_date.asc()).paginate(page=page, per_page=per_page).items
    return jsonify(concerts=[concert_simpl_schema.dump(i) for i in result])


@app.route('/concert/s/<string:concert_name>', methods=['GET'])
def get_concert_search(concert_name):
    result = Concert.query.filter(Concert.concert_name.ilike(f'%{concert_name}%'))
    if result is None:
        return jsonify(concerts=[])
    return jsonify(concerts=[concert_simpl_schema.dump(i) for i in result])


@app.route('/concert/<int:concert_id>', methods=['GET'])
def get_concert_by_id(concert_id):
    result = Concert.query.get(concert_id)
    if result is None:
        abort(404)
    return concert_schema.dump(result)


@app.route('/', methods=['GET'])
def get_start():
    return "Hello"


if True:
    from models import *

    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    # print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=1337)
