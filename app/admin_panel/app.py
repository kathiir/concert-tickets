from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import app

from admin_panel.routes import users, login, concerts, artists
if True:
    from models import *

    with app.app_context():
         db.create_all()

@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
