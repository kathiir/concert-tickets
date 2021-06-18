import traceback

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import asc
from config import app
from models import db, User


@app.route('/users', methods=['GET'])
def users_find():
    name_to_find = request.args.get("name")

    if name_to_find is None:
        name_to_find = ""

    name_search = "%{}%".format(name_to_find)

    all_rows = User.query \
        .filter(User.username.ilike(name_search)).order_by(asc(User.username))
    return render_template("users.html", users=all_rows.all())


@app.route('/users', methods=['GET'])
def users():
    all_users = User.query.order_by(asc(User.username)).all()
    return render_template("users.html", users=all_users)


@app.route('/users/ban', methods=['POST'])
def ban_user():
    try:
        curr_id = request.form.get('user_ID')
        User.query.filter(User.user_id == curr_id).update(
            {
                'user_role': 1
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
    return redirect(url_for('users'))


@app.route('/users/role', methods=['POST'])
def role_user():
    try:
        curr_id = request.form.get('user_ID')
        role = request.form.get('category')
        if (role == "Normal User"):
            User.query.filter(User.user_id == curr_id).update(
                {
                    'user_role': 0
                })
        elif (role == "Moderator"):
            User.query.filter(User.user_id == curr_id).update(
                {
                    'user_role': 2
                })
        elif (role == "Administrator"):
            User.query.filter(User.user_id == curr_id).update(
                {
                    'user_role': 3
                })
        elif (role == "Super Administrator"):
            User.query.filter(User.user_id == curr_id).update(
                {
                    'user_role': 4
                })
        db.session.commit()
    except Exception:
        traceback.print_exc()
    return redirect(url_for('users'))
