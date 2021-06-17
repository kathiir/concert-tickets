from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

db = SQLAlchemy()

Performance = db.Table(
    'performance',
    db.Column('performance_id', db.Integer, primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.artist_id')),
    db.Column('concert_id', db.Integer, db.ForeignKey('concert.concert_id'))
)

FavoriteArtists = db.Table(
    'favorite_artists',
    db.Column('favorite_artist_id', db.Integer, primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.artist_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'))
)

FavoriteConcerts = db.Table(
    'favorite_concerts',
    db.Column('favorite_concert_id', db.Integer, primary_key=True),
    db.Column('concert_id', db.Integer, db.ForeignKey('concert.concert_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'))
)


class City(db.Model):
    __tablename__ = 'city'
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), unique=False, nullable=False)
    halls = db.relationship('Hall', back_populates='city', lazy=True)  # one to many


class Hall(db.Model):
    __tablename__ = 'hall'
    hall_id = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(255), unique=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'))
    city = db.relationship('City', back_populates='halls', lazy=True)
    hall_zone = db.relationship('HallZone', back_populates='hall', order_by="desc(HallZone.price)", lazy=True)
    concert = db.relationship('Concert', back_populates='hall', lazy=True)


class HallZone(db.Model):
    __tablename__ = 'hall_zone'
    hall_zone_id = db.Column(db.Integer, primary_key=True)
    hall_zone_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.hall_id'), nullable=False)
    hall = db.relationship('Hall', back_populates='hall_zone', lazy=True)
    ticket = db.relationship('Ticket', back_populates='hall_zone', lazy=True)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, index=True)
    # placement = db.Column(db.Integer, unique=False, nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)
    concert = db.relationship('Concert', back_populates='ticket', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    user = db.relationship('User', back_populates='tickets', lazy=True)
    hall_zone_id = db.Column(db.Integer, db.ForeignKey('hall_zone.hall_zone_id'), nullable=False)
    hall_zone = db.relationship('HallZone', back_populates='ticket', lazy=True)


class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True, index=True)
    artist_genius_id = db.Column(db.String(100), unique=False, nullable=False)
    artist_spotify_id = db.Column(db.String(1000), unique=False, nullable=False)
    artist_name = db.Column(db.String(200), unique=False, nullable=False)
    artist_photo = db.Column(db.String(255), unique=False, nullable=True)
    performances = db.relationship('Concert', secondary=Performance, back_populates='performances',
                                   lazy=True)
    artist_reviews = db.relationship('ArtistReview', back_populates='artist', lazy=True)  # one to many
    favorite_artists = db.relationship('User', secondary=FavoriteArtists,
                                       back_populates='favorite_artists',
                                       lazy=True)  # many to many


class Concert(db.Model):
    __tablename__ = 'concert'
    concert_id = db.Column(db.Integer, primary_key=True, index=True)
    concert_name = db.Column(db.String(100), unique=False, nullable=False)
    concert_info = db.Column(db.String(1000), unique=False, nullable=True)
    concert_photo = db.Column(db.String(255), unique=False, nullable=True)
    concert_date = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.hall_id'), nullable=False)
    hall = db.relationship('Hall', back_populates='concert', lazy=True)
    concert_status = db.Column(db.Boolean, default=False, nullable=False) # false == open, true == cancelled
    performances = db.relationship('Artist', secondary=Performance, back_populates='performances')
    concert_reviews = db.relationship('ConcertReview', back_populates='concert', lazy=True)
    favorite_concerts = db.relationship('User', secondary=FavoriteConcerts, back_populates='favorite_concerts',
                                        lazy=True)
    ticket = db.relationship('Ticket', back_populates='concert', lazy=True)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), unique=False, nullable=False)
    user_role = db.Column(db.Integer, unique=False,
                          nullable=False)  # 0 - user, 1 - banned user, 2 - moderator, 3 - admin
    user_photo = db.Column(db.String(255), unique=False, nullable=True)  # base64 string
    user_email = db.Column(db.String(255), unique=True, nullable=False)

    user_token = db.Column(db.String(100), unique=True,
                           nullable=True)  # токен можно будет сделать по-жирнее
    user_token_exp_date = db.Column(db.DateTime, unique=False, nullable=True)

    user_spotify_refresh_token = db.Column(db.String(255), unique=False, nullable=True)
    user_spotify_access_token = db.Column(db.String(255), unique=False, nullable=True)
    user_spotify_token_exp_date = db.Column(db.DateTime, unique=False, nullable=True)

    user_google_refresh_token = db.Column(db.String(255), unique=False, nullable=True)
    user_google_access_token = db.Column(db.String(255), unique=False, nullable=True)
    user_google_token_exp_date = db.Column(db.DateTime, unique=False, nullable=True)

    concert_reviews = db.relationship('ConcertReview', back_populates='user', lazy=True)
    artist_reviews = db.relationship('ArtistReview', back_populates='user', lazy=True)
    favorite_artists = db.relationship('Artist', secondary=FavoriteArtists,
                                       back_populates='favorite_artists',
                                       lazy=True)  # many to many
    favorite_concerts = db.relationship('Concert', secondary=FavoriteConcerts,
                                        back_populates='favorite_concerts',
                                        lazy=True)
    tickets = db.relationship('Ticket', back_populates='user', lazy=True)


class ConcertReview(db.Model):
    __tablename__ = 'concert_review'
    concert_review_id = db.Column(db.Integer, primary_key=True, index=True)
    concert_review_info = db.Column(db.String(1000), unique=False, nullable=False)
    concert_review_rating = db.Column(db.Float, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship("User", back_populates="concert_reviews", lazy=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.concert_id'), nullable=False)
    concert = db.relationship("Concert", back_populates="concert_reviews", lazy=True)


class ArtistReview(db.Model):
    __tablename__ = 'artist_review'
    artist_review_id = db.Column(db.Integer, primary_key=True, index=True)
    artist_review_info = db.Column(db.String(1000), unique=False, nullable=False)
    artist_review_rating = db.Column(db.Float, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship("User", back_populates="artist_reviews", lazy=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)
    artist = db.relationship("Artist", back_populates="artist_reviews", lazy=True)


class IsExistsBoolField(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            return False

        return True


class CitySchema(SQLAlchemySchema):
    class Meta:
        model = City

    city_id = auto_field()
    city_name = auto_field()


class CitySimplifiedSchema(SQLAlchemySchema):
    class Meta:
        model = City

    city_id = auto_field()


class HallZoneSchema(SQLAlchemySchema):
    class Meta:
        model = HallZone

    hall_zone_id = auto_field()
    hall_zone_name = auto_field()
    price = auto_field()
    capacity = auto_field()


class HallSchema(SQLAlchemySchema):
    class Meta:
        model = Hall

    hall_id = auto_field()
    hall_name = auto_field()
    city = Nested(CitySchema, many=False)
    hall_zone = Nested(HallZoneSchema, many=True)


class HallSimplifiedSchema(SQLAlchemySchema):
    class Meta:
        model = Hall

    hall_id = auto_field()
    hall_name = auto_field()
    city = Nested(CitySchema, many=False)


class HallSuperSimplifiedSchema(SQLAlchemySchema): # only city
    class Meta:
        model = Hall

    hall_name = auto_field()
    city = Nested(CitySimplifiedSchema, many=False)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    username = auto_field()
    user_email = auto_field()
    user_photo = auto_field()
    user_spotify_token = IsExistsBoolField(attribute="user_spotify_refresh_token")
    user_gcalendar_token = IsExistsBoolField(attribute="user_google_refresh_token")


class UserSimplifiedSchema(SQLAlchemySchema):
    class Meta:
        model = User

    username = auto_field()
    user_photo = auto_field()


class ArtistReviewSchema(SQLAlchemySchema):
    class Meta:
        model = ArtistReview

    artist_review_id = auto_field()
    artist_review_info = auto_field()
    artist_review_rating = auto_field()
    user = Nested(UserSimplifiedSchema, many=False)


class ConcertReviewSchema(SQLAlchemySchema):
    class Meta:
        model = ConcertReview

    concert_review_id = auto_field()
    concert_review_info = auto_field()
    concert_review_rating = auto_field()
    user = Nested(UserSimplifiedSchema, many=False)


class ConcertSimplifiedSchema(SQLAlchemySchema):
    class Meta:
        model = Concert
        # include_relationships = True

    concert_id = auto_field()
    concert_name = auto_field()
    # concert_info = auto_field()
    concert_photo = auto_field()
    concert_date = auto_field()
    hall = Nested(HallSuperSimplifiedSchema, many=False)
    # city_id = auto_field()
    # creviews = db.relationship('ConcertReview', back_populates='concert', lazy=True)
    # favcon = db.relationship('FavoriteConcerts', back_populates='concert', lazy=True)
    # ticket = db.relationship('Ticket', back_populates='concert', lazy=True)


class ArtistSchema(SQLAlchemySchema):
    class Meta:
        model = Artist

    artist_id = auto_field()
    artist_genius_id = auto_field()
    artist_spotify_id = auto_field()
    artist_name = auto_field()
    artist_photo = auto_field()
    performances = Nested(ConcertSimplifiedSchema, many=True)
    # areviews = db.relationship('ArtistReview', back_populates='artist', lazy=True)
    # favart = db.relationship('FavoriteArtists', back_populates='artist', lazy=True)


class ArtistSimplifiedSchema(SQLAlchemySchema):
    class Meta:
        model = Artist

    artist_id = auto_field()
    # artist_genius_id = auto_field()
    # artist_spotify_id = auto_field()
    artist_name = auto_field()
    artist_photo = auto_field()
    # performances = auto_field()
    # areviews = db.relationship('ArtistReview', back_populates='artist', lazy=True)
    # favart = db.relationship('FavoriteArtists', back_populates='artist', lazy=True)


class ConcertSchema(SQLAlchemySchema):
    class Meta:
        model = Concert
        include_relationships = True

    concert_id = auto_field()
    concert_name = auto_field()
    concert_info = auto_field()
    concert_photo = auto_field()
    concert_date = auto_field()
    concert_status = auto_field()
    hall = Nested(HallSimplifiedSchema, many=False)
    performances = Nested(ArtistSimplifiedSchema, many=True)
    concert_reviews = Nested(ConcertReviewSchema, many =True)
    # favcon = db.relationship('FavoriteConcerts', back_populates='concert', lazy=True)
    # ticket = db.relationship('Ticket', back_populates='concert', lazy=True)


user_schema = UserSchema()
user_simpl_schema = UserSimplifiedSchema()

concert_schema = ConcertSchema()
artist_schema = ArtistSchema()

concert_simpl_schema = ConcertSimplifiedSchema()
artist_simpl_schema = ArtistSimplifiedSchema()

concert_review_schema = ConcertReviewSchema()
artist_review_schema = ArtistReviewSchema()

hall_schema = HallSchema()
hall_simpl_schema = HallSimplifiedSchema()

