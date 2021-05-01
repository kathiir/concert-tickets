import traceback

from flask import render_template, request, redirect, url_for, flash

from back import db, app
from models import Concert, Artist


@app.route('/artist', methods=['GET'])
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

    all_rows = Artist.query \
        .filter(Artist.artist_name.ilike(artist_name_search)) \
        .filter(Artist.artist_info.ilike(artist_info_search)) \
        .filter(Artist.artist_photo.ilike(artist_photo_search))
    return render_template("agents.html", agents=all_rows.all())  # ?


@app.route('/artist', methods=['GET'])
def artist():
    all_artist = Artist.query.all()
    return render_template("agents.html", agents=all_artist)  # ?


@app.route('/artist', methods=['POST'])
def add_artist():
    try:
        artist_name = request.form.get('newArtistName')
        artist_info = request.form.get('newArtistInfo')
        artist_photo = request.form.get('newArtistPhoto')
        new_artist = Artist(
            artist_name=artist_name,
            artist_info=artist_info,
            artist_photo=artist_photo
        )
        db.session.add(new_artist)
        db.session.commit()
    except Exception:
        flash('Этот артист уже добавлен!')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/artist/delete', methods=['POST'])
def delete_artist():
    artist_id = request.form.get('artist_id')
    try:
        del_artist = Artist.query.filter(Artist.artist_id == artist_id).first()
        db.session.delete(del_artist)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/artist/edit', methods=['POST'])
def edit_artist():
    try:
        curr_id = request.form.get('artist_id')
        Artist.query.filter(Artist.artist_id == curr_id).update(
            {
                'artist_name': request.form.get('artist_name'),
                'artist_info': request.form.get('artist_info'),
                'artist_photo': request.form.get('artist_photo'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))  # ?
