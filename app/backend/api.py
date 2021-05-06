from genius_api import Genius
from spotify_api import Spotify

genius = Genius()
spotify = Spotify()

print(genius.get_artist_info_by_id(1))

