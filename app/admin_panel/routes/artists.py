import traceback

from flask import render_template, request, redirect, url_for
from sqlalchemy import asc
from config import app
from models import db, Artist, ArtistReview, User


@app.route('/artists', methods=['GET'])
def artists_find():
    name_to_find = request.args.get("name")
    if name_to_find is None:
        name_to_find = ""

    name_search = "%{}%".format(name_to_find)

    all_rows = Artist.query \
        .filter(Artist.artist_name.ilike(name_search)).order_by(asc(Artist.artist_name))
    return render_template("artists.html", artists=all_rows.all())


@app.route('/artists', methods=['GET'])
def artists():
    all_artists = Artist.query.order_by(asc(Artist.concert_name)).all()
    return render_template("artists.html", artists=all_artists)


@app.route('/artists', methods=['POST'])
def add_artist():
    try:
        artist_name = request.form.get('newArtistName')
        artist_photo = request.form.get('newArtistPhoto')
        artist_genius_id = request.form.get('newArtistGenius')
        artist_spotify_id = request.form.get('newArtistSpotify')
        new_artist = Artist(
            artist_name=artist_name,
            artist_photo=artist_photo,
            artist_genius_id=artist_genius_id,
            artist_spotify_id=artist_spotify_id
        )
        db.session.add(new_artist)
        db.session.commit()
    except Exception:
        return redirect(url_for('artists'))
    return redirect(url_for('artists'))


@app.route('/artists/delete', methods=['POST'])
def delete_artist():
    artist_id = request.form.get('artist_ID')
    try:
        artist = Artist.query.filter(Artist.artist_id == artist_id).first()
        db.session.delete(artist)
        db.session.commit()
    except Exception:
        return redirect(url_for('artists'))
    return redirect(url_for('artists'))


@app.route('/artists/edit', methods=['POST'])
def edit_artist():
    try:
        curr_id = request.form.get('artist_ID')
        Artist.query.filter(Artist.artist_id == curr_id).update(
            {
                'artist_name': request.form.get('artist_name'),
                'artist_photo': request.form.get('artist_photo'),
                'artist_genius_id': request.form.get('artist_genius_id'),
                'artist_spotify_id': request.form.get('artist_spotify_id'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()

    return redirect(url_for('artists'))


@app.route('/artist_reviews/<int:id>', methods=['GET'])
def get_artist_reviews(id):
    artist = Artist.query.filter(Artist.artist_id == id).first()
    all_reviews = ArtistReview.query.filter(ArtistReview.artist_id == id).order_by(
        asc(ArtistReview.artist_review_id)).all()
    users = User.query.all()

    return render_template("artistreviews.html", artist_reviews=all_reviews, artist=artist, users=users)


@app.route('/artist_reviews/<int:id>/delete', methods=['POST'])
def artist_review_delete(id):
    try:
        id_review = request.form.get('artist_review')
        review = ArtistReview.query.filter(ArtistReview.artist_review_id == id_review).first()
        db.session.delete(review)
        db.session.commit()
    except Exception:
        return redirect(url_for('get_artist_reviews'))
    return redirect(url_for('get_artist_reviews', id=id))


@app.route('/artist_reviews/<int:id>/edit', methods=['POST'])
def edit_artist_review(id):
    try:
        id_review = request.form.get('artist_review')
        ArtistReview.query.filter(ArtistReview.artist_review_id == id_review).update(
            {
                'artist_review_info': request.form.get('artist_review_info'),
            })
        db.session.commit()
    except Exception:
        return redirect(url_for('get_artist_reviews'))
    return redirect(url_for('get_artist_reviews', id=id))
