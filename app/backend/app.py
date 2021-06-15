import json
from datetime import datetime

from flask import request, make_response, jsonify, abort
import os

from user_route import change_image, change_additional_user_token
from tickets import get_hall_with_zones, buy_tickets_mock, get_every_possible_ticket
from favorite_route import add_sth_to_favorite, remove_sth_to_favorite, is_sth_favorite, get_every_possible_favorites
from const_keys import SUCCESS_KEY
from very_complicated_logic import get_all_reviews, add_review_to_artist, get_all_info_about_concert, \
    add_review_to_concert, get_all_info_about_artist
from config import app
from genius_api import Genius
from spotify_api import Spotify

from auth_utils import register_user_with_response, login_user_by_login_and_pass, recreate_token_for_response, \
    change_passwd

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
    return json.dumps(response), 200, {'Content-Type': 'application/json'}


# login(email or login), password
@app.route('/login', methods=['POST'])
def login_user():
    data = simplify_json_result(
        request.get_json())  # костыль, так как надо сделать так, чтобы фронт не кидал списки вида: {'login': ['login']}
    response = login_user_by_login_and_pass(data['login'], data['password'])
    return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/pass_change', methods=['POST'])
def change_password():
    data = simplify_json_result(
        request.get_json())
    try:
        response = change_passwd(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}
    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), 400, {'Content-Type': 'application/json'}


@app.route('/user/photo', methods=['POST'])
def change_photo():
    data =  simplify_json_result(
        request.get_json())
    try:
        response = change_image(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}

    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), 400, {'Content-Type': 'application/json'}


@app.route('/user/additional_token', methods=['POST'])
def change_google_or_spotify_token():
    data = simplify_json_result(
        request.get_json())
    try:
        response = change_additional_user_token(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}

    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), 400, {'Content-Type': 'application/json'}


@app.route('/user_short_info/<string:token>', methods=['get'])
def user_short_info(token: str):
    response = {SUCCESS_KEY: True}

    response['user'] = user_simpl_schema.dump(db.session \
                                              .query(User) \
                                              .filter(User.user_token == token) \
                                              .first())
    if not response['user']:  # empty
        abort(404)

    response = recreate_token_for_response(response, token)
    return json.dumps(response), 200, {'Content-Type': 'application/json'}


# token
# returns: token (if expired), user, success (false if need to login)
@app.route('/user_profile/<string:token>', methods=['GET'])
def user_profile(token: str):
    response = {SUCCESS_KEY: True}

    response['user'] = user_schema.dump(db.session \
                                        .query(User) \
                                        .filter(User.user_token == token) \
                                        .first())
    if not response['user']:
        abort(404)

    response = recreate_token_for_response(response, token)
    return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    token = request.args.get('token')

    response = get_every_possible_favorites(token)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}


# id, type (artist, concert), token
# return success, token (if expires), description (if fail)
@app.route('/favorite/add', methods=['POST'])
def add_to_favorite():
    data = simplify_json_result(request.get_json())
    try:
        response = add_sth_to_favorite(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}

    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), 400, {'Content-Type': 'application/json'}


# id, type (artist, concert), token
# return success, token (if expires), description (if fail)
@app.route('/favorite/remove', methods=['DELETE'])
def remove_from_favorite():
    data = simplify_json_result(request.get_json())
    try:
        response = remove_sth_to_favorite(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}

    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), 400, {'Content-Type': 'application/json'}


# id, type (artist, concert)
# favorite, success, token (if expired), description (if fails)
@app.route('/favorite', methods=['GET'])
def get_is_favorite():
    data = request.args.to_dict()
    try:
        response = is_sth_favorite(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}

    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), 400, {'Content-Type': 'application/json'}


# id, type (artist, concert): лучше enum, но пофиг
# return list<review>, success
@app.route('/get_reviews/<string:query_type>/<int:id>', methods=['GET'])
def get_reviews(query_type, id):
    response = get_all_reviews(id,
                               query_type)

    if not response[SUCCESS_KEY]:
        return json.dumps(response), 400, {'Content-Type': 'application/json'}

    return json.dumps(response), 200, {'Content-Type': 'application/json'}


# token, artist_id, artist_review_info, artist_review_rating
# returns: success, description
@app.route('/add_artist_review', methods=['POST'])
def add_artist_review():
    data = simplify_json_result(request.get_json())
    try:
        response = add_review_to_artist(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}
    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), 400, {'Content-Type': 'application/json'}


@app.route('/artist/s/<string:artist_name>', methods=['GET'])
def get_artist_search(artist_name):
    result = Artist.query.filter(Artist.artist_name.ilike(f'%{artist_name}%'))
    if result is None:
        return jsonify(concerts=[])
    return jsonify(success=True,
                   artists=[artist_simpl_schema.dump(i) for i in result]), \
           200, \
           {'Content-Type': 'application/json'}


@app.route('/artist/<int:artist_id>', methods=['GET'])
def get_artist_by_id(artist_id):
    response = get_all_info_about_artist(artist_id,
                                         request.args.get('token'))
    if not response[SUCCESS_KEY]:
        abort(404)

    return json.dumps(response), \
           200, \
           {'Content-Type': 'application/json'}


@app.route('/concerts', methods=['GET'])
def get_concert_list():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    result = Concert.query

    if city_id := request.args.get('city_id'):

        result = result.join(Hall).join(City)\
            .filter(City.city_id == int(city_id))  # фласк сильно просил джоины, хотя работал

    result = result.filter(Concert.concert_date > datetime.now())\
        .order_by(Concert.concert_date.asc()) \
        .paginate(page=page, per_page=per_page).items

    return jsonify(success=True,
                   concerts=[concert_simpl_schema.dump(i) for i in result]), \
           200, \
           {'Content-Type': 'application/json'}


@app.route('/concert/s/<string:concert_name>', methods=['GET'])
def get_concert_search(concert_name):

    result = Concert.query

    if not 'show_all' in request.args.to_dict():
        result = result\
            .filter(Concert.concert_date > datetime.now())

    if city_id := request.args.get('city_id'):

        result = result.join(Hall).join(City)\
            .filter(City.city_id == int(city_id))  # получил джоины за хорошую работу ¯\_(ツ)_/¯

    result = result \
        .order_by(Concert.concert_date.asc())\
        .filter(Concert.concert_name.ilike(f'%{concert_name}%'))

    if result is None:
        return jsonify(success=True, concerts=[])
    return jsonify(success=True,
                   concerts=[concert_simpl_schema.dump(i) for i in result]), \
           200, \
           {'Content-Type': 'application/json'}


# id, token
# returns: success, description(if failed),
#           concert_average_mark, concert_is_ended
#           concert: concert_name, concert_reviews (better to look for results in postman)
@app.route('/concert/<int:concert_id>', methods=['GET'])
def get_concert_by_id(concert_id):
    response = get_all_info_about_concert(concert_id,
                                          request.args.get('token'))
    if not response[SUCCESS_KEY]:
        abort(404)
    return json.dumps(response), \
           200, \
           {'Content-Type': 'application/json'}


# token, concert_id, concert_review_info, concert_review_rating
# returns: success, description
@app.route('/add_concert_review', methods=['POST'])
def add_concert_review():
    data = simplify_json_result(request.get_json())
    try:
        response = add_review_to_concert(data)
        return json.dumps(response), 200, {'Content-Type': 'application/json'}
    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), \
               400, \
               {'Content-Type': 'application/json'}


# id
# returns success
@app.route('/hall/<int:hall_id>', methods=['GET'])
def get_hall_info(hall_id: int):
    hall = db.session.query(Hall) \
        .filter(Hall.hall_id == hall_id) \
        .first()

    if not hall:
        abort(404)

    return json.dumps({SUCCESS_KEY: True, 'hall': hall_schema.dump(hall)}), \
           200, \
           {'Content-Type': 'application/json'}


@app.route('/concert_tickets/<int:concert_id>', methods=['GET'])
def get_with_zones_by_concert_id(concert_id: int):
    response = get_hall_with_zones(concert_id)

    if not response[SUCCESS_KEY]:
        abort(404)

    return json.dumps(response), \
           200, \
           {'Content-Type': 'application/json'}


@app.route('/buy_tickets', methods=['POST'])
def buy_tickets():
    data = simplify_json_result(request.get_json())
    try:
        response = buy_tickets_mock(data)

        return json.dumps(response),\
               200, \
               {'Content-Type': 'application/json'}

    except ValueError:
        return json.dumps({SUCCESS_KEY: False}), \
               400, \
               {'Content-Type': 'application/json'}


@app.route('/get_user_tickets', methods=['GET'])
def get_tickets_by_user():
    token = request.args.get('token')

    response = get_every_possible_ticket(token)
    return json.dumps(response), \
           200, \
           {'Content-Type': 'application/json'}


# @app.route("/swagger")
# def spec():
#     return jsonify(swagger(app))


@app.route('/', methods=['GET'])
def get_start():
    return '''
        ,----,
   ___.`      `,
   `===  D     :
     `'.      .'
        )    (    Hello World!   ,
       /      \_________________/|
      /                          |
     |                           ;
     |               _____       /
     |      \       ______7    ,'
     |       \    ______7     /
      \       `-,____7      ,'   jgs
^~^~^~^`\                  /~^~^~^~^
  ~^~^~^ `----------------' ~^~^~^
 ~^~^~^~^~^^~^~^~^~^~^~^~^~^~^~^~
''', 200, {"content-type": "text/plain"}


if True:
    from models import *

    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    # print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=1337)
