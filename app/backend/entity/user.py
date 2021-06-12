import traceback

from flask import render_template, request, redirect, url_for, flash

from config import app
from models import User, db


@app.route('/user', methods=['GET'])
def user_find():
    username_to_find = request.args.get("username")
    user_password_to_find = request.args.get("user_password")
    user_role_to_find = request.args.get("user_role")
    user_photo_to_find = request.args.get("user_photo")
    user_spotify_token_to_find = request.args.get("user_spotify_token")
    user_gcalendar_token_to_find = request.args.get("user_gcalendar_token")

    if username_to_find is None:
        username_to_find = ""
    if user_password_to_find is None:
        user_password_to_find = ""
    if user_role_to_find is None:
        user_role_to_find = ""
    if user_photo_to_find is None:
        user_photo_to_find = ""
    if user_spotify_token_to_find is None:
        user_spotify_token_to_find = ""
    if user_gcalendar_token_to_find is None:
        user_gcalendar_token_to_find = ""

    username_search = "%{}%".format(username_to_find)
    user_password_search = "%{}%".format(user_password_to_find)
    user_role_search = "%{}%".format(user_role_to_find)
    user_photo_search = "%{}%".format(user_photo_to_find)
    user_spotify_token_search = "%{}%".format(user_spotify_token_to_find)
    user_gcalendar_token_search = "%{}%".format(user_gcalendar_token_to_find)

    all_rows = User.query \
        .filter(User.username.ilike(username_search)) \
        .filter(User.user_password.ilike(user_password_search)) \
        .filter(User.user_role.ilike(user_role_search)) \
        .filter(User.user_photo.ilike(user_photo_search)) \
        .filter(User.user_spotify_token.ilike(user_spotify_token_search)) \
        .filter(User.user_gcalendar_token.ilike(user_gcalendar_token_search))
    return render_template("agents.html", agents=all_rows.all())


@app.route('/user', methods=['GET'])
def user():
    all_user = User.query.all()
    return render_template("agents.html", agents=all_user)


@app.route('/user', methods=['POST'])
def add_user():
    try:
        username_to_find = request.form.get('username')
        user_password_to_find = request.form.get('newUserPassword')
        user_role_to_find = request.form.get('newUserRole')
        user_photo_to_find = request.form.get('newUserPhoto')
        user_spotify_token_to_find = request.form.get('newUserSpotifyToken')
        user_gcalendar_token_to_find = request.form.get('newUserGcalendarToken')
        new_user = User(
            username_to_find=username_to_find,
            user_password_to_find=user_password_to_find,
            user_role_to_find=user_role_to_find,
            user_photo_to_find=user_photo_to_find,
            user_spotify_token_to_find=user_spotify_token_to_find,
            user_gcalendar_token_to_find=user_gcalendar_token_to_find
        )
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        flash('Этот пользователь уже добавлен!')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/user/delete', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    try:
        del_user = User.query.filter(User.user_id == user_id).first()
        db.session.delete(del_user)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/user/edit', methods=['POST'])
def edit_user():
    try:
        curr_id = request.form.get('user_id')
        User.query.filter(User.user_id == curr_id).update(
            {
                'username': request.form.get('username'),
                'user_password': request.form.get('user_password'),
                'user_role': request.form.get('user_role'),
                'user_photo': request.form.get('user_photo'),
                'user_spotify_token': request.form.get('user_spotify_token'),
                'user_gcalendar_token': request.form.get('user_gcalendar_token'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))
