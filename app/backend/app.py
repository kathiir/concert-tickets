import traceback

from flask import Flask, request, make_response, jsonify, abort
import os
import re

from werkzeug.security import generate_password_hash

from config import app
from models import db
from models import Concert, Artist, concert_schema, artist_schema, concert_simpl_schema, artist_simpl_schema, User, user_simpl_schema
from genius_api import Genius
from spotify_api import Spotify
from urllib.parse import unquote

genius = Genius()
spotify = Spotify()


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


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


@app.route('/users', methods=['POST'])
def post_new_user():
    data = list(filter(None, re.split('email=|&password=|&password_check=', unquote(request.get_data()))))
    email = data[0]
    try:
        password1 = data[1]
        password2 = data[2]
        user = User.query.filter(User.user_email == email).first()

        if user is not None:
            return jsonify({'result': 'email'})

        if password1 != password2:
            return jsonify({'result': 'password'})

        hash_password = generate_password_hash(password1)
        new_user = User(
            username = email,
            user_email=email,
            user_password=hash_password,
            user_role = 0,
        )
        db.session.add(new_user)
        db.session.commit()

    except Exception:
        user = User.query.filter(User.user_email == email).first()
        db.session.delete(user)
        db.session.commit()
        traceback.print_exc()

    return jsonify({'result': 'success'})

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


@app.route('/', methods=['GET'])
def get_start():
    return "Hello"

if True:
    from models import *

    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1337))
    print(' http://127.0.0.1:1337/')
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=1337)

