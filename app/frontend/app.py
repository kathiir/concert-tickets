import datetime
import json

import requests
import os
from flask import request, render_template, abort, redirect, url_for, session, jsonify
from flask_cors import cross_origin

from config import app, babel, back_uri, cloud
import cloudinary.uploader


@app.template_filter('dt')
def _jinja2_filter_datetime(date):
    ret = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%d %B %Y %H:%M')
    return ret


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


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


@app.route('/')
def index_page():
    request_uri = back_uri + '/concerts'
    response = requests.get(request_uri)
    jason = response.json()['concerts']

    return render_template(
        'index.html',
        concerts=jason
    )


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if 'logged_in' in session and session['logged_in']:
        redirect(request.referrer)
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        request_uri = back_uri + 'login'
        response = requests.post(request_uri, json=data).json()

        if response['success']:
            session['logged_in'] = True
            session['token'] = response['token']
            request_uri = back_uri + 'user_short_info/' + response['token']
            response = requests.get(request_uri).json()
            if response['success']:
                session['username'] = response['user']['username']
                session['user_photo'] = response['user']['user_photo']
            return redirect(url_for('index_page'))

    return render_template(
        'login.html'
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index_page'))


@app.route('/registration', methods=["GET", "POST"])
def registration_page():
    if 'logged_in' in session and session['logged_in']:
        redirect(request.referrer)
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
            if response['success']:
                session['username'] = response['user']['username']
                session['user_photo'] = response['user']['user_photo']
            return redirect(url_for('index_page'))

    return render_template(
        'registration.html', messages=messages
    )


# TODO
@app.route('/tickets')
def tickets_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(request.referrer)

    # request_uri = back_uri + 'user_short_info/' + res['token']
    # response = requests.get(request_uri).json()
    return render_template(
        'tickets.html'
    )


# TODO
@app.route('/favorites')
def favorites_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(request.referrer)


    return render_template(
        'favorites.html'
    )


@app.route('/settings', methods=["GET", "POST"])
@cross_origin()
def settings_page():
    messages = []
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(request.referrer)
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
                    messages.append('Successfully changed user image')
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
                messages.append('Successfully changed password')
                if 'token' in response:
                    session['token'] = response['token']
            else:
                messages.append('Failed to set new password')

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
    request_uri = back_uri + '/concert/s/' + request.args.get('search')
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


@app.route('/concert/<int:id>')
def concert_page(id):
    request_uri = back_uri + '/concert/' + str(id)
    response = requests.get(request_uri)
    if response.status_code != 200:
        abort(404)
    concert = response.json()

    return render_template(
        'concert.html',
        concert=concert
    )


@app.route('/artists/<int:id>')
def artists_page(id):
    request_uri = back_uri + '/artist/' + str(id)
    response = requests.get(request_uri)
    if response.status_code != 200:
        abort(404)
    artist = response.json()

    return render_template(
        'artist.html',
        artist=artist
    )


@app.route('/ticket/<int:id>', methods=['GET', 'POST'])
def buy_page(id):
    # request_uri = back_uri + '/artist/' + str(id)
    # response = requests.get(request_uri)
    # if response.status_code != 200:
    #     abort(404)
    # artist = response.json()
    palette = ['#F58634', '#FFCC29', '#81B214', '#206A5D']

    if request.method == 'POST':
        return redirect(url_for('buying_confirm_page', success='success', id=id))

    return render_template(
        'buying.html',
        palette=palette
    )


@app.route('/buying_confirm/<int:id>/<success>')
def buying_confirm_page(success, id):
    # if 'logged_in' not in session or not session['logged_in']:
    #     return redirect(request.referrer)
    if success == 'success':
        success = True
    else:
        success = False
    return render_template(
        'buying_confirm.html',
        success=success,
        id=id
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
