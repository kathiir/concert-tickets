import traceback

from flask import render_template, request, redirect, url_for, flash

from config import app
from models import ConcertReview, db


@app.route('/creview', methods=['GET'])
def creview_find():
    creview_info_to_find = request.args.get("creview_info")
    creview_rating_to_find = request.args.get("creview_rating")

    if creview_info_to_find is None:
        creview_info_to_find = ""
    if creview_rating_to_find is None:
        creview_rating_to_find = ""

    creview_info_search = "%{}%".format(creview_info_to_find)
    creview_rating_search = "%{}%".format(creview_rating_to_find)

    all_rows = ConcertReview.query \
        .filter(ConcertReview.сreview_info.ilike(creview_info_search)) \
        .filter(ConcertReview.creview_rating.ilike(creview_rating_search))
    return render_template("agents.html", agents=all_rows.all())  # ?


@app.route('/creview', methods=['GET'])
def creview():
    all_creview = ConcertReview.query.all()
    return render_template("agents.html", agents=all_creview)  # ?


@app.route('/creview', methods=['POST'])
def add_creview():
    try:
        creview_info = request.form.get('newConcertReviewInfo')
        creview_rating = request.form.get('newConcertReviewRating')
        new_creview = ConcertReview(
            creview_info=creview_info,
            creview_rating=creview_rating
        )
        db.session.add(new_creview)
        db.session.commit()
    except Exception:
        flash('Это ревью уже добавлено!')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/creview/delete', methods=['POST'])
def delete_creview():
    creview_id = request.form.get('creview_id')
    try:
        del_creview = ConcertReview.query.filter(ConcertReview.creview_id == creview_id).first()
        db.session.delete(del_creview)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/creview/edit', methods=['POST'])
def edit_creview():
    try:
        curr_id = request.form.get('creview_id')
        ConcertReview.query.filter(ConcertReview.creview_id == curr_id).update(
            {
                'creview_info': request.form.get('creview_info'),
                'creview_rating': request.form.get('creview_rating'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))  # ?
