from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
# from config import app

db = SQLAlchemy()

Performance = db.Table(
    'performance',
    db.Column('performance_id', db.Integer, primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.artist_id')),
    db.Column('concert_id', db.Integer, db.ForeignKey('concert.concert_id'))
)


class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True, index=True)
    artist_genius_id = db.Column(db.String(100), unique=False, nullable=False)
    artist_spotify_id = db.Column(db.String(1000), unique=False, nullable=False)
    artist_name = db.Column(db.String(200), unique=False, nullable=False)
    artist_photo = db.Column(db.String(300), unique=False, nullable=True)
    performances = db.relationship('Concert', secondary=Performance, viewonly=True, backref='artist')
    areviews = db.relationship('ArtistReview', backref='artist', lazy=True)
    favart = db.relationship('FavoriteArtists', backref='artist', lazy=True)


class City(db.Model):
    __tablename__ = 'city'
    city_id = db.Column(db.Integer, primary_key=True, index=True)
    city_name = db.Column(db.String(100), unique=False, nullable=False)
    hall = db.relationship('Hall', backref='city', lazy=True)


class Concert(db.Model):
    __tablename__ = 'concert'
    concert_id = db.Column(db.Integer, primary_key=True, index=True)
    concert_name = db.Column(db.String(100), unique=False, nullable=False)
    concert_info = db.Column(db.String(1000), unique=False, nullable=True)
    concert_photo = db.Column(db.String(300), unique=False, nullable=True)
    concert_date = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.hall_id'), nullable=False)
    concert_status_id = db.Column(db.Integer, db.ForeignKey('concert_status.concert_status_id'), nullable=False)
    performances = db.relationship('Artist', secondary=Performance, viewonly=True, backref='concert')
    creviews = db.relationship('ConcertReview', backref='concert', lazy=True)
    favcon = db.relationship('FavoriteConcerts', backref='concert', lazy=True)
    ticket = db.relationship('Ticket', backref='concert', lazy=True)


class ConcertStatus(db.Model):
    __tablename__ = 'concert_status'
    concert_status_id = db.Column(db.Integer, primary_key=True, index=True)
    concert_status_name = db.Column(db.String(100), unique=False, nullable=False)
    concert = db.relationship('Concert', backref='concert_status', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), unique=False, nullable=False)
    user_role = db.Column(db.Integer, unique=False, nullable=False)
    user_photo = db.Column(db.String(100), unique=False, nullable=True)  # base64 string
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_token = db.Column(db.String(64), unique=True, nullable=True) # при регистрации уже токен делаем, зачем тогда nullable?
    user_token_exp_date = db.Column(db.DateTime, unique=False, nullable=True)
    user_spotify_token = db.Column(db.String(100), unique=False, nullable=True)
    user_gcalendar_token = db.Column(db.String(100), unique=False, nullable=True)
    activity = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    creviews = db.relationship('ConcertReview', backref='users', lazy=True)
    areviews = db.relationship('ArtistReview', backref='users', lazy=True)
    favart = db.relationship('FavoriteArtists', backref='users', lazy=True)
    favcon = db.relationship('FavoriteConcerts', backref='users', lazy=True)
    ticket = db.relationship('Ticket', backref='users', lazy=True)

    def is_active(self):
        return self.activity


class Hall(db.Model):
    __tablename__ = 'hall'
    hall_id = db.Column(db.Integer, primary_key=True, index=True)
    hall_name = db.Column(db.String(100), unique=True, nullable=False)
    hall_address = db.Column(db.String(1000), unique=False, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    hall_zone = db.relationship('HallZone', backref='hall', lazy=True)
    concert = db.relationship('Concert', backref='hall', lazy=True)


class HallZone(db.Model):
    __tablename__ = 'hall_zone'
    hall_zone_id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    hall_zone_name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer, primary_key=True, index=True)
    capacity = db.Column(db.Integer, primary_key=True, index=True)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.hall_id'), nullable=False)
    ticket = db.relationship('Ticket', backref='hall_zone', lazy=True)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, index=True)
    placement = db.Column(db.Integer, unique=False, nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    hall_zone_id = db.Column(db.Integer, db.ForeignKey('hall_zone.hall_zone_id'), nullable=False)


class ConcertReview(db.Model):
    __tablename__ = 'concert_review'
    creview_id = db.Column(db.Integer, primary_key=True, index=True)
    creview_info = db.Column(db.String(1000), unique=False, nullable=False)
    creview_rating = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)


class ArtistReview(db.Model):
    __tablename__ = 'artist_review'
    areview_id = db.Column(db.Integer, primary_key=True, index=True)
    areview_info = db.Column(db.String(1000), unique=False, nullable=False)
    areview_rating = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)


class FavoriteArtists(db.Model):
    __tablename__ = 'favorite_artists'
    favart_id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'artist_id'),
    )


class FavoriteConcerts(db.Model):
    __tablename__ = 'favorite_concerts'
    favart_id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'concert_id'),
    )


class ConcertSimplifiedSchema(SQLAlchemySchema):
    class Meta:
        model = Concert
        # include_relationships = True

    concert_id = auto_field()
    concert_name = auto_field()
    # concert_info = auto_field()
    concert_photo = auto_field()
    concert_date = auto_field()
    #concert_address = auto_field()
    #city_id = auto_field()
    # creviews = db.relationship('ConcertReview', backref='concert', lazy=True)
    # favcon = db.relationship('FavoriteConcerts', backref='concert', lazy=True)
    # ticket = db.relationship('Ticket', backref='concert', lazy=True)


class ArtistSchema(SQLAlchemySchema):
    class Meta:
        model = Artist

    artist_id = auto_field()
    artist_genius_id = auto_field()
    artist_spotify_id = auto_field()
    artist_name = auto_field()
    artist_photo = auto_field()
    performances = Nested(ConcertSimplifiedSchema, many=True)
    # areviews = db.relationship('ArtistReview', backref='artist', lazy=True)
    # favart = db.relationship('FavoriteArtists', backref='artist', lazy=True)


class ArtistSimplifiedSchema(SQLAlchemySchema):
    class Meta:
        model = Artist

    artist_id = auto_field()
    # artist_genius_id = auto_field()
    # artist_spotify_id = auto_field()
    artist_name = auto_field()
    artist_photo = auto_field()
    # performances = auto_field()
    # areviews = db.relationship('ArtistReview', backref='artist', lazy=True)
    # favart = db.relationship('FavoriteArtists', backref='artist', lazy=True)


class ConcertSchema(SQLAlchemySchema):
    class Meta:
        model = Concert
        # include_relationships = True

    concert_id = auto_field()
    concert_name = auto_field()
    # concert_info = auto_field()
    concert_photo = auto_field()
    concert_date = auto_field()
    #concert_address = auto_field()
    #city_id = auto_field()
    performances = Nested(ArtistSimplifiedSchema, many=True)
    # creviews = db.relationship('ConcertReview', backref='concert', lazy=True)
    # favcon = db.relationship('FavoriteConcerts', backref='concert', lazy=True)
    # ticket = db.relationship('Ticket', backref='concert', lazy=True)


concert_schema = ConcertSchema()
artist_schema = ArtistSchema()
concert_simpl_schema = ConcertSimplifiedSchema()
artist_simpl_schema = ArtistSimplifiedSchema()
