import json

from flask import Flask, request, make_response, jsonify, abort
import os

from config import app, login_manager
from models import db
from models import Concert, Artist, concert_schema, artist_schema, concert_simpl_schema, artist_simpl_schema, User
from genius_api import Genius
from spotify_api import Spotify

from auth_utils import register_user_with_responce, login_user_by_login_and_pass
from utils import simplify_json_result

genius = Genius()
spotify = Spotify()



@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#nickname, email, password, password_check
@app.route('/registration', methods=['POST'])
def register_user():
    data = simplify_json_result(request.get_json())
    responce = register_user_with_responce(data)
    return json.dumps(responce), 200, {'ContentType':'application/json'}


#login(email or login), password
@app.route('/login', methods=['POST'])
def login_user():
    data = simplify_json_result(request.get_json()) # костыль, так как надо сделать так, чтобы фронт не кидал списки вида: {'login': ['login']}
    responce = login_user_by_login_and_pass(data['login'], data['password'])
    return json.dumps(responce), 200, {'ContentType':'application/json'}


#token
@app.route('/user_info', methods=['POST'])
def token_gen():
    data = simplify_json_result(request.get_json())
    #token (если обновляем), user


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

### Точно пока не знаю, надо ли это ###
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

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

