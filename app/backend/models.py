from back import db

class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    info = db.Column(db.String(1000), unique=True, nullable=False)
    photo = db.Column(db.String(100), unique=True, nullable=False) #base64 string