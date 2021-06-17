import datetime
import os
import urllib.parse

import cloudinary.uploader
import requests
from flask import request, render_template, abort, redirect, url_for, session
from flask_babel import gettext
from flask_cors import cross_origin

from config import app, babel, back_uri, cloud
from google_front import get_google_auth_url_stateful, get_google_credentials_stateful
from spotify_front import get_spotify_auth_url, pass_response


@app.template_filter('dt')
def _jinja2_filter_datetime(date):
    ret = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%d %B %Y %H:%M')
    return ret


@babel.localeselector
def get_locale():
    if 'locale' in session:
        return session['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/change_locale')
def change_locale():
    if 'locale' in session:
        if session['locale'] == 'ru':
            session['locale'] = 'en'
        else:
            session['locale'] = 'ru'
    else:
        session['locale'] = 'ru'
    return redirect(request.referrer)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/city')
@app.route('/city/<int:id>')
def change_city(id=1):
    if id > 3 or id < 1:
        session['city'] = 1
    else:
        session['city'] = id
    return redirect(request.referrer)


@app.route('/favorite/artist/<int:id>')
def add_artist_to_favorite(id):
    data = {'token': session['token'],
            'type': 'artist',
            'id': id
            }
    request_uri = back_uri + 'favorite/add'
    response = requests.post(request_uri, json=data).json()
    if 'token' in response:
        session['token'] = response['token']
    return redirect(request.referrer)


@app.route('/unfavorite/artist/<int:id>')
def remove_artist_from_favorite(id):
    data = {'token': session['token'],
            'type': 'artist',
            'id': id
            }
    request_uri = back_uri + 'favorite/remove'
    request_uri += f"?{urllib.parse.urlencode(data)}"
    response = requests.delete(request_uri).json()
    if 'token' in response:
        session['token'] = response['token']
    return redirect(request.referrer)


@app.route('/favorite/concert/<int:id>')
def add_concert_to_favorite(id):
    data = {'token': session['token'],
            'type': 'concert',
            'id': id
            }
    request_uri = back_uri + 'favorite/add'
    response = requests.post(request_uri, json=data).json()
    if 'token' in response:
        session['token'] = response['token']
    return redirect(request.referrer)


@app.route('/unfavorite/concert/<int:id>')
def remove_concert_from_favorite(id):
    data = {'token': session['token'],
            'type': 'concert',
            'id': id
            }
    request_uri = back_uri + 'favorite/remove'
    request_uri += f"?{urllib.parse.urlencode(data)}"
    response = requests.delete(request_uri).json()
    if 'token' in response:
        session['token'] = response['token']
    return redirect(request.referrer)


@app.route('/')
def index_page():
    request_uri = back_uri + '/concerts?per_page=100&' + 'city_id=' + (
        str(session['city']) if 'city' in session else str(1))
    response = requests.get(request_uri)
    jason = response.json()['concerts']
    spot = []
    if 'logged_in' in session and session['logged_in']:
        if 'spotify' in session and session['spotify']:
            request_uri = back_uri + '/user_followed_concerts?token=' + session['token']
            response = requests.get(request_uri).json()
            spot = response['concerts']
            if 'token' in response:
                session['token'] = response['token']

    return render_template(
        'index.html',
        concerts=jason,
        spotify=spot
    )


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index_page'))
    messages = []
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        request_uri = back_uri + 'login'
        response = requests.post(request_uri, json=data).json()

        if response['success']:
            session['logged_in'] = True
            session['token'] = response['token']
            request_uri = back_uri + 'user_profile/' + response['token']
            response = requests.get(request_uri).json()
            if response['success']:
                session['username'] = response['user']['username']
                session['user_photo'] = response['user']['user_photo']
                session['g_calendar'] = response['user']['user_gcalendar_token']
                session['spotify'] = response['user']['user_spotify_token']

            if request.form.get('remember'):
                session.permanent = True
            return redirect(url_for('index_page'))

        else:
            messages.append(gettext('Incorrect login or password'))

    return render_template(
        'login.html', messages=messages
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index_page'))


@app.route('/registration', methods=["GET", "POST"])
def registration_page():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index_page'))
    messages = []
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        request_uri = back_uri + 'registration'
        response = requests.post(request_uri, json=data)
        res = response.json()

        if res['success']:
            session['logged_in'] = True
            session['token'] = res['token']
            request_uri = back_uri + 'user_short_info/' + res['token']
            response = requests.get(request_uri).json()
            session['g_calendar'] = False
            session['spotify'] = False
            if response['success']:
                session['username'] = response['user']['username']
                session['user_photo'] = response['user']['user_photo']

            if request.form.get('remember'):
                session.permanent = True
            return redirect(url_for('index_page'))

        else:
            if 'email' in res:
                messages.append(gettext('This email already exists'))
            if 'nickname' in res:
                messages.append(gettext('This login already exists'))

    return render_template(
        'registration.html', messages=messages
    )


@app.route('/tickets')
def tickets_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    tickets = []

    request_uri = back_uri + 'get_user_tickets?token=' + session['token']
    response = requests.get(request_uri).json()
    if response['success']:
        tickets = response['tickets']
        if 'token' in response:
            session['token'] = response['token']

    return render_template(
        'tickets.html', tickets=tickets
    )


@app.route('/favorites')
def favorites_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    request_uri = back_uri + 'favorites?token=' + session['token']
    response = requests.get(request_uri).json()

    if 'token' in response:
        session['token'] = response['token']

    concerts = response['concerts']
    artists = response['artists']

    return render_template(
        'favorites.html', concerts=concerts, artists=artists
    )


@app.route('/settings', methods=["GET", "POST"])
@cross_origin()
def settings_page():
    messages = []
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        if 'image-change' in request.form:
            file_to_upload = request.files['img']
            if file_to_upload:
                upload_result = cloud.uploader.upload(file_to_upload)

                jason = upload_result
                image_url = jason['url']
                data = {'token': session['token'], 'user_photo': image_url}
                request_uri = back_uri + 'user/photo'
                response = requests.post(request_uri, json=data).json()
                if response['success']:
                    messages.append(gettext('Successfully changed user image'))
                    session['user_photo'] = image_url
                    if 'token' in response:
                        session['token'] = response['token']
                else:
                    messages.append('Failed to set user image')
        elif 'password-change' in request.form:
            data = request.form.to_dict(flat=False)
            data['token'] = session['token']
            request_uri = back_uri + 'pass_change'
            response = requests.post(request_uri, json=data).json()
            if response['success']:
                messages.append(gettext('Successfully changed password'))
                if 'token' in response:
                    session['token'] = response['token']
            else:
                messages.append(gettext('Failed to set new password'))

    request_uri = back_uri + 'user_profile/' + session['token']
    response = requests.get(request_uri).json()
    if 'token' in response:
        session['token'] = response['token']
    if response['success']:
        session['username'] = response['user']['username']
        session['user_photo'] = response['user']['user_photo']
        session['g_calendar'] = response['user']['user_gcalendar_token']
        session['spotify'] = response['user']['user_spotify_token']

    return render_template(
        'settings.html', messages=messages
    )


@app.route('/about')
def about_page():
    return render_template(
        'about.html'
    )


@app.route('/contacts')
def contacts_page():
    return render_template(
        'contacts.html'
    )


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    request_uri = back_uri + '/concert/s/' + request.args.get('search') + '?city_id=' + \
                  (str(session['city']) if 'city' in session else str(1))
    response = requests.get(request_uri)
    concerts = response.json()['concerts']

    request_uri = back_uri + '/artist/s/' + request.args.get('search')
    response = requests.get(request_uri)
    artists = response.json()['artists']

    return render_template(
        'search.html',
        concerts=concerts,
        artists=artists
    )


@app.route('/concert/<int:id>', methods=["GET", "POST"])
def concert_page(id):
    request_uri = back_uri + 'concert/' + str(id)
    if 'logged_in' in session and session['logged_in']:
        request_uri = request_uri + '?token=' + session['token']
        if request.method == 'POST':
            data = {
                "token": session['token'],
                "concert_id": id,
                "concert_review_info": request.form.get('info'),
                "concert_review_rating": request.form.get('rate')
            }
            review_uri = back_uri + 'add_concert_review'
            response = requests.post(review_uri, json=data).json()
            if 'token' in response:
                session['token'] = response['token']
    response = requests.get(request_uri)
    if response.status_code != 200:
        abort(404)

    concert = response.json()

    if 'token' in concert:
        session['token'] = concert['token']

    request_uri = back_uri + 'get_reviews/concert/' + str(id)
    response = requests.get(request_uri).json()
    reviews = response['list']

    return render_template(
        'concert.html',
        concert=concert,
        reviews=reviews
    )


@app.route('/artists/<int:id>', methods=["GET", "POST"])
def artists_page(id):
    request_uri = back_uri + 'artist/' + str(id)
    if 'logged_in' in session and session['logged_in']:
        request_uri = request_uri + '?token=' + session['token']
        if request.method == 'POST':
            data = {
                "token": session['token'],
                "artist_id": id,
                "artist_review_info": request.form.get('info'),
                "artist_review_rating": request.form.get('rate')
            }
            review_uri = back_uri + 'add_artist_review'
            response = requests.post(review_uri, json=data).json()
            if 'token' in response:
                session['token'] = response['token']
    response = requests.get(request_uri)
    if response.status_code != 200:
        abort(404)

    artist = response.json()

    if 'token' in artist:
        session['token'] = artist['token']

    request_uri = back_uri + 'get_reviews/artist/' + str(id)
    response = requests.get(request_uri).json()
    reviews = response['list']
    return render_template(
        'artist.html',
        artist=artist,
        reviews=reviews
    )


@app.route('/ticket/<int:id>', methods=['GET', 'POST'])
def buy_page(id):
    request_uri = back_uri + 'concert_tickets/' + str(id)

    response = requests.get(request_uri)
    if response.status_code != 200:
        abort(404)
    halls = response.json()

    if request.method == 'POST':
        request_uri = back_uri + 'buy_tickets'
        data = {
            "concert_id": id,
            "hall_zone": []
        }
        f = request.form
        for h in halls['hall_zone']:
            ar = f['h' + str(h['hall_zone_id'])]
            zone = {
                "hall_zone_id": str(h['hall_zone_id']),
                "amount": ar
            }
            data['hall_zone'].append(zone)

        if 'logged_in' in session and session['logged_in']:
            data['token'] = session['token']

        response = requests.post(request_uri, json=data, headers={'Content-Type': 'application/json'}).json()

        if 'token' in response:
            session['token'] = response['token']

        if response['success']:
            return redirect(url_for('buying_confirm_page', success='success', id=id))
        else:
            return redirect(url_for('buying_confirm_page', success='failure', id=id))

    palette = ['#F58634', '#FFCC29', '#81B214', '#206A5D']

    return render_template(
        'buying.html',
        palette=palette,
        halls=halls
    )


@app.route('/buying_confirm/<int:id>/<success>')
def buying_confirm_page(success, id):
    if success == 'success':
        success = True
    else:
        success = False
    return render_template(
        'buying_confirm.html',
        success=success,
        id=id
    )


@app.route('/spotipy')
def spotipy():
    if 'token' in session:
        return redirect(get_spotify_auth_url(session['token']))

    return 400


@app.route('/spotipy/callback')
def spotipy_callback():
    req = request.args.to_dict()

    try:
        response = pass_response(req)

        if 'token' in response:
            session['logged_in'] = True
            session['token'] = response['token']

        if response:
            response = requests.post(back_uri + "user/additional_token", json=response)
            response = response.json()

            session['spotify'] = True
            session.modified = True
            return redirect(url_for('settings_page'))

    except ValueError:
        return 400


@app.route('/spotipy/remove')
def remove_spotipy():
    session['spotify'] = False
    data = {'token': session['token'],
            'type': 'spotify'
            }
    request_uri = back_uri + 'user/additional_token'
    request_uri += f"?{urllib.parse.urlencode(data)}"
    response = requests.delete(request_uri).json()
    if 'token' in response:
        session['token'] = response['token']
    return redirect(url_for('settings_page'))


@app.route('/google')
def google():
    redirect_uri = url_for('google_callback', _external=True)
    url, state = get_google_auth_url_stateful(redirect_uri, "state")
    return redirect(url)


@app.route('/google/callback')
def google_callback():
    try:
        if 'token' in session:
            redirect_uri = url_for('google_callback', _external=True)
            response = get_google_credentials_stateful(request.url, redirect_uri, 'state')

            if response:
                response['token'] = session['token']
                response = requests.post(back_uri + "user/additional_token", json=response)
                response = response.json()

                if 'token' in response:
                    session['token'] = response['token']

                session['gcalendar'] = True
                return redirect(url_for('settings_page'))

    except:
        return redirect(url_for('settings_page'))


@app.route('/add_to_gcalendar/<int:id>')
def add_to_gcalendar(id):
    request_uri = back_uri + 'add_to_calendar'
    data = {
        "concert_id": id,
        "token": session['token']
    }
    response = requests.post(request_uri, json=data).json()
    if 'token' in response:
        session['token'] = response['token']

    if response['success']:
        return render_template('calendar_confirm.html', success='success', id=id)
    else:
        return render_template('calendar_confirm.html', success='failure', id=id)


@app.route('/google/remove')
def remove_google():
    session['gcalendar'] = False
    data = {'token': session['token'],
            'type': 'google'
            }
    request_uri = back_uri + 'user/additional_token'
    request_uri += f"?{urllib.parse.urlencode(data)}"
    response = requests.delete(request_uri).json()
    if 'token' in response:
        session['token'] = response['token']
    return redirect(url_for('settings_page'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' https://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port,
            ssl_context=('cert.pem', 'key.pem'))  # TODO
