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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
    # app.run()
