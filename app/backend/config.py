from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = '''postgresql+psycopg2://akuflasmffmhkm:c6c41cb1973ddb103db56d98962800c0fed938c979fdbdd04dc5e1172f567ae6@ec2-52-19-170-215.eu-west-1.compute.amazonaws.com:5432/d6eddr59h6ok4t
'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'LKGHJghjksdkhjglfjhklsdhgkfhgkFKGHJDFdgjljkh;h;ljkskhgdfghklshjlk;'
db.init_app(app)
