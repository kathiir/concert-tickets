from back import db


class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True, index=True)
    artist_name = db.Column(db.String(100), unique=False, nullable=False)
    artist_info = db.Column(db.String(1000), unique=False, nullable=False)
    artist_photo = db.Column(db.String(100), unique=False, nullable=False)  # base64 string
    performances = db.relationship('Performance', backref='artist', lazy=True)
    areviews = db.relationship('ArtistReview', backref='artist', lazy=True)
    favart = db.relationship('FavoriteArtists', backref='artist', lazy=True)


class Concert(db.Model):
    __tablename__ = 'concert'
    concert_id = db.Column(db.Integer, primary_key=True, index=True)
    concert_name = db.Column(db.String(100), unique=False, nullable=False)
    concert_info = db.Column(db.String(1000), unique=False, nullable=False)
    concert_photo = db.Column(db.String(100), unique=False, nullable=False)  # base64 string
    concert_date = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    performances = db.relationship('Performance', backref='concert', lazy=True)
    creviews = db.relationship('ConcertReview', backref='concert', lazy=True)
    favcon = db.relationship('FavoriteConcerts', backref='concert', lazy=True)
    ticket = db.relationship('Ticket', backref='concert', lazy=True)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), unique=False, nullable=False)
    user_role = db.Column(db.Integer, unique=False, nullable=False)
    user_photo = db.Column(db.String(100), unique=False, nullable=False)  # base64 string
    user_spotify_token = db.Column(db.String(100), unique=False, nullable=True)
    user_gcalendar_token = db.Column(db.String(100), unique=False, nullable=True)
    creviews = db.relationship('ConcertReview', backref='user', lazy=True)
    areviews = db.relationship('ArtistReview', backref='user', lazy=True)
    favart = db.relationship('FavoriteArtists', backref='user', lazy=True)
    favcon = db.relationship('FavoriteConcerts', backref='user', lazy=True)
    ticket = db.relationship('Ticket', backref='user', lazy=True)


class Hall(db.Model):
    __tablename__ = 'hall'
    hall_id = db.Column(db.Integer, primary_key=True, index=True)
    hall_name = db.Column(db.String(100), unique=True, nullable=False)
    hall_address = db.Column(db.String(100), unique=True, nullable=False)
    ticket = db.relationship('Ticket', backref='hall', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, index=True)
    placement = db.Column(db.Integer, unique=False, nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.hall_id'), nullable=False)

class Performance(db.Model):
    __tablename__ = 'performance'
    performance_id = db.Column(db.Integer, primary_key=True, index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)


class ConcertReview(db.Model):
    __tablename__ = 'concert_review'
    creview_id = db.Column(db.Integer, primary_key=True, index=True)
    сreview_info = db.Column(db.String(1000), unique=False, nullable=False)
    creview_rating = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)


class ArtistReview(db.Model):
    __tablename__ = 'artist_review'
    areview_id = db.Column(db.Integer, primary_key=True, index=True)
    areview_info = db.Column(db.String(1000), unique=False, nullable=False)
    areview_rating = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)


class FavoriteArtists(db.Model):
    __tablename__ = 'favorite_artists'
    favart_id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'artist_id'),
    )


class FavoriteConcerts(db.Model):
    __tablename__ = 'favorite_concerts'
    favart_id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'concert_id'),
    )
