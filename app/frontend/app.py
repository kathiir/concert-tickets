from flask import Flask, request, render_template
import os
from flask_babel import Babel
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['LANGUAGES'] = {
    'en': 'English',
    'ru': 'Russian'
}

bootstrap = Bootstrap(app)
babel = Babel(app)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/')
def index_page():
    return render_template(
        'index.html'
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
    return render_template(
        'search.html'
    )


@app.route('/concert/<int:id>')
def concert_page(id):
    return render_template(
        'concert.html',
        concert_id=id
    )


@app.route('/artists/<int:id>')
def artists_page(id):
    return render_template(
        'artist.html',
        concert_id=id
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
    # app.run()
