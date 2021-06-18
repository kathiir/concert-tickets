import traceback

from flask import render_template, request, redirect, url_for
from sqlalchemy import asc
from config import app
from models import db, Concert, ConcertReview, User


@app.template_filter('dt')
def _jinja2_filter_datetime(date):
    ret = date.strftime('%d %B %Y %H:%M')
    return ret


@app.route('/сoncerts', methods=['GET'])
def concerts_find():
    name_to_find = request.args.get("name")

    if name_to_find is None:
        name_to_find = ""

    name_search = "%{}%".format(name_to_find)

    all_rows = Concert.query \
        .filter(Concert.concert_name.ilike(name_search)).order_by(asc(Concert.concert_name))
    return render_template("concerts.html", concerts=all_rows.all())


@app.route('/concerts', methods=['GET'])
def concerts():
    all_concerts = Concert.query.order_by(asc(Concert.concert_name)).all()
    return render_template("concerts.html", concerts=all_concerts)


@app.route('/concerts/edit', methods=['POST'])
def edit_concert():
    try:
        curr_id = request.form.get('concert_ID')
        Concert.query.filter(Concert.concert_id == curr_id).update(
            {
                'concert_info': request.form.get('concert_info'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()

    return redirect(url_for('concerts'))


@app.route('/concerts/status', methods=['POST'])
def concert_status():
    try:
        curr_id = request.form.get('concert_ID')
        status = request.form.get('status')
        if (status == "Waited"):
            Concert.query.filter(Concert.concert_id == curr_id).update(
                {
                    'concert_status': False
                })
        elif (status == "Ended"):
            Concert.query.filter(Concert.concert_id == curr_id).update(
                {
                    'concert_status': True
                })
        db.session.commit()
    except Exception:
        traceback.print_exc()
    return redirect(url_for('concerts'))


@app.route('/reviews/<int:id>', methods=['GET'])
def get_reviews(id):
    concert = Concert.query.filter(Concert.concert_id == id).first()
    all_reviews = ConcertReview.query.filter(ConcertReview.concert_id == id).order_by(
        asc(ConcertReview.concert_review_id)).all()
    users = User.query.all()

    return render_template("concertreviews.html", concert_reviews=all_reviews, concert=concert, users=users)


@app.route('/reviews/<int:id>/delete', methods=['POST'])
def review_delete(id):
    try:
        id_review = request.form.get('concert_review')
        review = ConcertReview.query.filter(ConcertReview.concert_review_id == id_review).first()
        db.session.delete(review)
        db.session.commit()
    except Exception:
        return redirect(url_for('get_reviews'))
    return redirect(url_for('get_reviews', id=id))


@app.route('/reviews/<int:id>/edit', methods=['POST'])
def edit_review(id):
    try:
        id_review = request.form.get('concert_review')
        ConcertReview.query.filter(ConcertReview.concert_review_id == id_review).update(
            {
                'concert_review_info': request.form.get('concert_review_info'),
            })
        db.session.commit()
    except Exception:
        return redirect(url_for('get_reviews'))
    return redirect(url_for('get_reviews', id=id))
