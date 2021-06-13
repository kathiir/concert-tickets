import os

from flask import request, make_response, jsonify, abort

from config import app
from genius_api import Genius
from spotify_api import Spotify

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

