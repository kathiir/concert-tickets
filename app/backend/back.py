from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = '''postgresql+psycopg2://akuflasmffmhkm:c6c41cb1973ddb103db56d98962800c0fed938c979fdbdd04dc5e1172f567ae6@ec2-52-19-170-215.eu-west-1.compute.amazonaws.com:5432/d6eddr59h6ok4t
'''
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