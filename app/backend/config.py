from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:11111111@localhost:5432/concertHall"
login_manager = LoginManager()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'LKGHJghjksdkhjglfjhklsdhgkfhgkFKGHJDFdgjljkh;h;ljkskhgdfghklshjlk;'
db.init_app(app)
