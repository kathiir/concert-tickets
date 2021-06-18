import os

from flask import render_template

from config import app

from routes import users, login, concerts, artists

if True:
    from models import *

    with app.app_context():
        db.create_all()


@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
