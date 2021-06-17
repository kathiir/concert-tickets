import datetime
import os
import random

from flask import jsonify

from config import app, db
from genius_api import Genius
from models import Concert
from spotify_api import Spotify


def get_date():
    start_date = datetime.datetime(2021, 5, 6)
    end_date = datetime.datetime(2021, 12, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    half_hours = random.randrange(14, 48)
    # datetime.timedelta(seconds=half_hours*1800)

    random_date = start_date + datetime.timedelta(days=random_number_of_days) + datetime.timedelta(
        seconds=half_hours * 1800)
    return random_date



g = Genius()
s = Spotify()

a = []


# # for art in artists:
# #     # print(s.get_artist_id_by_name(art))
# #     # print(g.get_artist_id_by_name(art))
# #
# #     artist_genius_id = g.get_artist_id_by_name(art)
# #     artist_spotify_id = s.get_artist_id_by_name(art)
# #     print(artist_genius_id)
# #     print(artist_spotify_id)
# #
# #     new_artist = Artist(
# #         artist_genius_id=artist_genius_id,
# #         artist_spotify_id=artist_spotify_id
# #     )
# #     a.append(new_artist)
# #     time.sleep(1)
#
#
@app.route('/', methods=['GET'])
def get_concerts():
    # task = filter(lambda t: t['id'] == task_id, tasks)

    ar = []

    all = Concert.query.all()

    for i, c in enumerate(all):
        c.concert_photo = c.performances[0].artist_photo
        if i % 10 == 0:
            db.session.commit()

    # for n in range(555):
    #     art = Artist.query.get(n + 1)
    #     if art.artist_spotify_id != '0':
    #         gen = s.get_artist_image_by_id(art.artist_spotify_id)
    #         art.artist_photo = gen
    #         ar.append(gen)
    #         print(gen)
    #         if n % 10 == 0:
    #             db.session.commit()

    db.session.commit()

    # ar = concert_schema.dump(ar)
    # if len(all_concert) == 0:
    # abort(404)
    return jsonify(ar)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
