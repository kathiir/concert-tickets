import datetime
import requests
import os
from flask import Flask, request, render_template, abort
from flask_babel import Babel


back_uri = 'https://concert-hall-back.herokuapp.com'
# back_uri = 'http://127.0.0.1:5005/'

app = Flask(__name__)
app.config['LANGUAGES'] = {
    'en': 'English',
    'ru': 'Russian'
}

babel = Babel(app)


@app.template_filter('dt')
def _jinja2_filter_datetime(date):
    ret = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%d %B %Y %H:%M')
    return ret


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/city/<int:id>')
def change_city(id):
    # if city is valid
    # session['city'] = 123
    return render_template(request.referrer)


@app.route('/')
def index_page():
    request_uri = back_uri + '/concerts'
    response = requests.get(request_uri)
    jason = response.json()['concerts']

    return render_template(
        'index.html',
        concerts=jason
    )


@app.route('/login')
def login_page():
    return render_template(
        'login.html'
    )


@app.route('/registration')
def registration_page():
    return render_template(
        'registration.html'
    )


@app.route('/tickets')
def tickets_page():
    return render_template(
        'tickets.html'
    )


@app.route('/favorites')
def favorites_page():
    return render_template(
        'favorites.html'
    )


@app.route('/settings')
def settings_page():
    return render_template(
        'settings.html'
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
