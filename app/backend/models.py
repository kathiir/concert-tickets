from back import db

class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(100), unique=False, nullable=False)
    artist_info = db.Column(db.String(1000), unique=False, nullable=False)
    artist_photo = db.Column(db.String(100), unique=False, nullable=False) #base64 string

class Concert(db.Model):
    __tablename__ = 'concert'
    concert_id = db.Column(db.Integer, primary_key=True)
    concert_name = db.Column(db.String(100), unique=False, nullable=False)
    concert_info = db.Column(db.String(1000), unique=False, nullable=False)
    concert_photo = db.Column(db.String(100), unique=False, nullable=False) #base64 string

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), unique=False, nullable=False)
    user_role = db.Column(db.Integer, unique=False, nullable=False)
    user_photo = db.Column(db.String(100), unique=False, nullable=False) #base64 string
    user_spotify_token = db.Column(db.String(100), unique=False, nullable=True)
    user_gcalendar_token = db.Column(db.String(100), unique=False, nullable=True)