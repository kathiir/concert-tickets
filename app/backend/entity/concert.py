import traceback

from flask import render_template, request, redirect, url_for, flash

from back import db, app
from models import Concert


@app.route('/concert', methods=['GET'])
def agents_find():
    artist_name_to_find = request.args.get("artist_name")
    artist_info_to_find = request.args.get("artist_info")
    artist_photo_to_find = request.args.get("artist_photo")

    if artist_name_to_find is None:
        artist_name_to_find = ""
    if artist_info_to_find is None:
        artist_info_to_find = ""
    if artist_photo_to_find is None:
        artist_photo_to_find = ""

    artist_name_search = "%{}%".format(artist_name_to_find)
    artist_info_search = "%{}%".format(artist_info_to_find)
    artist_photo_search = "%{}%".format(artist_photo_to_find)

    all_rows = Concert.query \
        .filter(Concert.artist_name.ilike(artist_name_search)) \
        .filter(Concert.artist_info.ilike(artist_info_search)) \
        .filter(Concert.artist_photo.ilike(artist_photo_search))
    return render_template("agents.html", agents=all_rows.all())  # ?


@app.route('/concert', methods=['GET'])
def concert():
    all_concert = Concert.query.all()
    return render_template("agents.html", agents=all_concert)  # ?


@app.route('/concert', methods=['POST'])
def add_concert():
    try:
        concert_name = request.form.get('newConcertArtistName')
        concert_info = request.form.get('newConcertArtistInfo')
        concert_photo = request.form.get('newConcertArtistPhoto')
        new_concert = Concert(
            concert_name=concert_name,
            concert_info=concert_info,
            concert_photo=concert_photo
        )
        db.session.add(new_concert)
        db.session.commit()
    except Exception:
        flash('Этот концерт уже добавлен!')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/concert/delete', methods=['POST'])
def delete_concert():
    concert_id = request.form.get('concert_id')
    try:
        del_concert = Concert.query.filter(Concert.concert_id == concert_id).first()
        db.session.delete(del_concert)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/concert/edit', methods=['POST'])
def edit_concert():
    try:
        curr_id = request.form.get('concert_id')
        Concert.query.filter(Concert.concert_id == curr_id).update(
            {
                'concert_name': request.form.get('concert_name'),
                'concert_info': request.form.get('concert_info'),
                'concert_photo': request.form.get('concert_photo'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))  # ?
