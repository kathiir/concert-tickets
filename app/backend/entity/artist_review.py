import traceback

from flask import render_template, request, redirect, url_for, flash

from config import app
from models import ArtistReview, db


@app.route('/areview', methods=['GET'])
def areview_find():
    areview_info_to_find = request.args.get("areview_info")
    areview_rating_to_find = request.args.get("areview_rating")

    if areview_info_to_find is None:
        areview_info_to_find = ""
    if areview_rating_to_find is None:
        areview_rating_to_find = ""

    areview_info_search = "%{}%".format(areview_info_to_find)
    areview_rating_search = "%{}%".format(areview_rating_to_find)

    all_rows = ArtistReview.query \
        .filter(ArtistReview.areview_info.ilike(areview_info_search)) \
        .filter(ArtistReview.areview_rating.ilike(areview_rating_search))
    return render_template("agents.html", agents=all_rows.all())


@app.route('/areview', methods=['GET'])
def areview():
    all_areview = ArtistReview.query.all()
    return render_template("agents.html", agents=all_areview)


@app.route('/areview', methods=['POST'])
def add_areview():
    try:
        areview_info = request.form.get('newArtistReviewInfo')
        areview_rating = request.form.get('newArtistReviewRating')
        new_areview = ArtistReview(
            areview_info=areview_info,
            areview_rating=areview_rating
        )
        db.session.add(new_areview)
        db.session.commit()
    except Exception:
        flash('Это ревью уже добавлено!')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/areview/delete', methods=['POST'])
def delete_areview():
    areview_id = request.form.get('areview_id')
    try:
        del_areview = ArtistReview.query.filter(ArtistReview.areview_id == areview_id).first()
        db.session.delete(del_areview)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/areview/edit', methods=['POST'])
def edit_areview():
    try:
        curr_id = request.form.get('areview_id')
        ArtistReview.query.filter(ArtistReview.areview_id == curr_id).update(
            {
                'areview_info': request.form.get('areview_info'),
                'areview_rating': request.form.get('areview_rating'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))
