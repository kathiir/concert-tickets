from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456789@localhost:5432/concertHall'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'LKGHJghjksdkhjglfjhklsdhgkfhgkFKGHJDFdgjljkh;h;ljkskhgdfghklshjlk;'
db = SQLAlchemy()
db.init_app(app)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

if True:

    from models import *
    with app.app_context():
        db.create_all()


@app.route('/')
def hello_world():
    return 'Мир вам, земляне!'


if __name__ == '__main__':
    app.run()