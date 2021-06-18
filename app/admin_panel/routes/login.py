import hashlib

from flask import render_template, request, redirect, url_for, session
from sqlalchemy import or_
from config import app
from models import db, User


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if 'logged_in' in session and session['logged_in']:
        redirect(request.referrer)
    if request.method == 'POST':
        check = False
        data = request.form.to_dict(flat=False)
        user_login = request.form.get("login")
        passwd = request.form.get("password")
        user = db.session.query(User) \
            .filter(or_(user_login == User.user_email, user_login == User.username)) \
            .first()
        user_role = db.session.query(User.user_role).filter_by(username=user_login).scalar()
        if not user or not check_pass(passwd, user.user_password) or user_role < 2:
            check = False
            return redirect(url_for('login_page'))

        db.session.add(user)
        db.session.commit()
        check = True
        if check:
            session['logged_in'] = True
            session['role'] = user_role
            session['username'] = user_login
            return redirect(url_for('users'))
        else:
            return redirect(url_for('login_page'))

    return render_template(
        'login.html'
    )


@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")


def check_pass(passwd: str, passwd_with_hash: str) -> bool:
    passwd_hash = passwd_with_hash.split('@', 2)[0]
    salt = passwd_with_hash.split('@', 2)[1]

    if hash_password_using_salt(passwd, salt) == passwd_hash:
        return True

    return False


def hash_password_using_salt(passwd: str, salt: str):
    assert len(salt) == 32
    assert len(passwd) > 7

    passwd_len = len(passwd)
    passwd_with_salt = salt[:4] \
                       + passwd[:int(passwd_len / 2)] \
                       + salt[4: 12] \
                       + passwd[-int(passwd_len / 2 + passwd_len % 2):] \
                       + salt[-4:]

    return hashlib.sha256(passwd_with_salt.encode()).hexdigest()
