import time

from flask import Flask, request, make_response, jsonify, abort
import os
from config import app, db
from models import Concert, Artist, concert_schema

import datetime
import random
from genius_api import Genius
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


for i in range(10):
    print(get_date())

artists = ['10cc', '2Pac', '50 Cent', 'A Thousand Horses', 'ABBA', 'ABC', 'Aerosmith', 'Agnetha Fältskog',
           'Alan Jackson',
           'Albert King', 'Alice Cooper', 'Alison Krauss', 'The All-American Rejects', 'The Allman Brothers Band',
           'Amy Winehouse', 'Andre Rieu', 'Andrea Bocelli', 'Andrew W.K.', 'Anthrax', 'Antonio Carlos Jobim',
           'Apache Indian', 'Arcade Fire', 'Ariana Grande', 'Arrested Development', 'Ashley Campbell',
           'Astrud Gilberto',
           'Aswad', 'Atlanta Rhythm Section', 'Audioslave', 'B.B. King', 'Badfinger', 'The Band',
           'Barclay James Harvest',
           'Barry White', 'The Beach Boys', 'Beastie Boys', 'The Beatles', 'Beck', 'Bee Gees', 'Belinda Carlisle',
           'Ben Harper', 'Ben Howard', 'Benny Andersson', 'Big Country', 'Big Star', 'Bill Evans', 'Billie Holiday',
           'Billy Currington', 'Billy Fury', 'Billy Preston', 'Björk', 'Black Eyed Peas', 'Black Sabbath',
           'Black Uhuru',
           'Blind Faith', 'Blink-182', 'Blondie', 'Blue Cheer', 'Bo Diddley', 'Bob Dylan', 'Bob Marley', 'Bon Jovi',
           'Bonnie Raitt', 'Booker T', 'Boyz II Men', 'Brantley Gilbert', 'Brenda Holloway', 'Brian Eno',
           'The Brothers Johnson', 'Bruce Springsteen', 'Bryan Adams', 'Bryan Ferry', 'Buddy Guy', 'Buddy Holly',
           'Burning Spear', 'Burt Bacharach', 'The Cadillac Three', 'Camel', 'Canned Heat', 'Captain Beefheart',
           'Caravan',
           'Carpenters', 'Cat Stevens', 'Charlie Parker', 'Cheap Trick', 'The Chemical Brothers', 'Cher',
           'Chris Cornell',
           'Chris Stapleton', 'Chuck Berry', 'Cinderella', 'The Clash', 'Climax Blues Band', 'Coleman Hawkins',
           'Commodores', 'Common', 'The Common Linnets', 'Corinne Bailey Rae', 'Count Basie', 'Counting Crows',
           'Craig Armstrong', 'The Cranberries', 'Cream', 'Creedence Clearwater Revival', 'Crowded House',
           'Culture Club',
           'The Cure', 'Cutting Crew', 'D’Angelo', 'DMX', 'The Damned', 'Daniel Hope', 'Danny Wilson & Gary Clark',
           'David Bowie', 'Dean Martin', 'Debarge', 'Deep Purple', 'Def Leppard', 'Demi Lovato', 'Demis Roussos',
           'Derek And The Dominos', 'Desmond Dekker', 'Diana Krall', 'Diana Ross', 'Diana Ross & The Supremes',
           'Dierks Bentley', 'Dinah Washington', 'Dio', 'Dire Straits', 'Disclosure', 'Don Henley', 'Donna Summer',
           'The Doors', 'Dr Dre', 'Drake', 'Duke Ellington', 'Dusty Springfield', 'EELS', 'EPMD', 'Eagles',
           'Eagles Of Death Metal', 'Eazy-E', 'Eddie Cochran', 'Elbow', 'Ella Fitzgerald', 'Elliott Smith',
           'Elton John',
           'Elvis Costello', 'Elvis Presley', 'Emeli Sandé', 'Eminem', 'Enigma', 'Eric B. & Rakim', 'Eric Church',
           'Eric Clapton', 'Etta James', 'Evanescence', 'Eve', 'Extreme', 'Fairport Convention', 'Fats Domino', 'Faust',
           'Fergie', 'Florence + The Machine', 'The Flying Burrito Brothers', 'Four Tops', 'Foxy Brown',
           'Frank Sinatra',
           'Frank Zappa', 'Frankie Goes To Hollywood', 'Freddie Mercury', 'Free', 'Frida Lyngstad', 'The Game',
           'Gang Starr', 'Gary Moore', 'Gene Krupa', 'Gene Vincent', 'Genesis', 'Gentle Giant', 'George Benson',
           'George Harrison', 'George Michael', 'George Strait', 'George Thorogood', 'Georgie Fame', 'Ghostface Killah',
           'Ginger Baker', 'Glen Campbell', 'Gong', 'Grace Jones', 'Graham Parker', 'Grand Funk Railroad',
           'Gregory Isaacs',
           'Gregory Porter', 'Guns N’ Roses', 'Gwen Stefani', 'Hank Williams', 'Heart', 'Heaven 17', 'Helmet',
           'Herbie Hancock', 'Hoobastank', 'Howlin Wolf', 'Hoyt Axton', 'Huey Lewis & The News', 'The Human League',
           'Humble Pie', 'INXS', 'Ice Cube', 'Iggy Pop', 'Imagine Dragons', 'Iron Maiden', 'Isaac Hayes',
           'The Isley Brothers', 'It Bites', 'J.J. Cale', 'Jack Bruce', 'Jack Johnson', 'Jackson 5', 'Jacques Brel',
           'Jadakiss', 'The Jam', 'James', 'James Bay', 'James Blake', 'James Brown', 'James Morrison', 'James Taylor',
           'Jane’s Addiction', 'Janet Jackson', 'Japan & David Sylvian', 'Jay-Z', 'Jeezy', 'Jeru the Damaja',
           'Jessie J',
           'Jimi Hendrix', 'Jimmy Buffett', 'Jimmy Cliff', 'Jimmy Eat World', 'Jimmy Ruffin', 'Jimmy Smith',
           'Joan Armatrading', 'Joan Baez', 'Joe Cocker', 'Joe Jackson', 'Joe Sample', 'Joe Walsh / The James Gang',
           'John Coltrane', 'John Fogerty', 'John Lee Hooker', 'John Lennon', 'John Martyn', 'John Mayall',
           'John Mellencamp', 'John Williams', 'Johnny Cash', 'Johnny Gill', 'Joni Mitchell', 'Jonny Lang',
           'Joss Stone',
           'Jr. Walker & The All Stars', 'Julie London', 'Jurassic 5', 'Justin Bieber', 'Kacey Musgraves',
           'Kaiser Chiefs',
           'Kanye West', 'Kate Bush', 'Katy Perry', 'Keane', 'Keith Jarrett', 'Keith Richards', 'Keith Urban',
           'Kendrick Lamar', 'Kenny Burrell', 'Kevin Coyne', 'The Killers', 'Killing Joke', 'Kim Carnes', 'The Kinks',
           'Kip Moore', 'Kiss', 'The Kooks', 'Kool And The Gang', 'LL Cool J', 'Lady A', 'Lady GaGa', 'Lana Del Rey',
           'Laura Marling', 'Led Zeppelin', 'Lee ‘Scratch’ Perry', 'Lenny Kravitz', 'Leon Russell', 'Lester Young',
           'Level 42', 'The Libertines', 'Lightnin’ Hopkins', 'Lil Wayne', 'Linton Kwesi Johnson', 'Lionel Richie',
           'Little Big Town', 'Little Richard', 'Lloyd Cole', 'Lorde', 'Louis Armstrong', 'Lucinda Williams',
           'Ludacris',
           'Ludovico Einaudi', 'Luke Bryan', 'Lulu', 'The Lumineers', 'Lynyrd Skynyrd', 'Maddie & Tae', 'Madonna',
           'Magazine', 'The Mamas & The Papas', 'Marc Almond', 'Marilyn Manson', 'Mark Knopfler', 'Maroon 5',
           'Martha Reeves & The Vandellas', 'The Marvelettes', 'Marvin Gaye', 'Mary Hopkin', 'Mary J. Blige',
           'Mary Wells',
           'Massive Attack', 'Master P', 'The Mavericks', 'Maxi Priest', 'McCoy Tyner', 'Meat Loaf', 'Megadeth',
           'Melody Gardot', 'Metallica', 'Method Man', 'Michael Jackson', 'Michael Nyman', 'Mike & the Mechanics',
           'Mike Oldfield', 'Miles Davis', 'Minnie Riperton', 'The Moody Blues', 'Morrissey', 'Motörhead',
           'Muddy Waters',
           'Mumford & Sons', 'Mötley Crüe', 'N.W.A', 'Nanci Griffith', 'Nas', 'Nat King Cole', 'Nazareth', 'Ne-Yo',
           'Neil Diamond', 'Neil Young', 'Nelly', 'Neneh Cherry', 'New Edition', 'New York Dolls', 'Nick Drake',
           'Nicki Minaj', 'Nik Kershaw', 'Nina Simone', 'Nine Inch Nails', 'Nirvana', 'The Nitty Gritty Dirt Band',
           'No Doubt', 'Norah Jones', 'OMD', 'Ocean Colour Scene', 'OneRepublic', 'Onyx', 'Oscar Peterson',
           'Otis Redding',
           'The Ozark Mountain Daredevils', 'PJ Harvey', 'Papa Roach', 'Pat Benatar', 'Pato Banton', 'Patsy Cline',
           'Patty Griffin', 'Paul McCartney and Wings', 'Paul Simon', 'Paul Weller', 'Peaches & Herb', 'Pearl Jam',
           'Peggy Lee', 'Pete Townshend', 'Peter Frampton', 'Phil Collins', 'Phil Manzanera', 'PiL (Public Image Ltd)',
           'Pink Floyd', 'Placebo', 'Poco', 'Poison', 'The Police', 'Portishead', 'Prince', 'Public Enemy', 'Pulp',
           'Queen',
           'Queens Of The Stone Age', 'Quicksilver Messenger Service', 'Quincy Jones', 'R.E.M.', 'Rainbow', 'Rammstein',
           'Ray Charles', 'Reba McEntire', 'Red Hot Chili Peppers', 'Redman', 'Richie Havens', 'Rick James',
           'Rick Nelson',
           'Rick Ross', 'Rick Wakeman', 'The Righteous Brothers', 'Rihanna', 'Ringo Starr', 'Rise Against',
           'Rob Zombie',
           'Robbie Williams', 'Robert Cray', 'Robert Glasper', 'Robert Palmer', 'Robert Plant', 'Rod Stewart',
           'Roger Daltrey', 'The Rolling Stones', 'Ronnie Lane', 'Ronnie Wood', 'Rory Gallagher', 'The Roots',
           'Rosanne Cash', 'Roxy Music', 'Roy Orbison', 'Ruff Ryders', 'Rufus Wainwright', 'Rush', 'The Ruts',
           'Saint Etienne', 'Salt-n-Pepa', 'Sam Cooke', 'Sam Hunt', 'Sam Smith', 'Sammy Hagar', 'Sandy Denny',
           'Schiller',
           'Scorpions', 'Scott Walker', 'Secret Garden', 'Sensational Alex Harvey Band', 'Serge Gainsbourg',
           'Sergio Mendes', 'Sex Pistols', 'Shaggy', 'Sham 69', 'Shania Twain', 'Sheryl Crow', 'Simple Minds',
           'Siouxsie & The Banshees', 'Slayer', 'Slick Rick', 'Sly & Robbie', 'Small Faces', 'The Smashing Pumpkins',
           'Smokey Robinson', 'Smokey Robinson & The Miracles', 'Snoop Dogg', 'Snow Patrol', 'Soft Cell', 'Sonic Youth',
           'Sonny Boy Williamson', 'Soul II Soul', 'Soundgarden', 'Spandau Ballet', 'Sparks', 'Spice Girls',
           'Stan Getz',
           'The Statler Brothers', 'Status Quo', 'Steel Pulse', 'Steely Dan', 'Steppenwolf', 'Stereo MCs',
           'Stereophonics',
           'Steve Earle', 'Steve Hackett', 'Steve Hillage', 'Steve Miller Band', 'Steve Winwood', 'Steven Tyler',
           'Stevie Wonder', 'Sting', 'The Style Council', 'Styx', 'Sublime', 'Sum 41', 'Supertramp', 'Suzanne Vega',
           'T-Bone Walker', 'T. Rex', 'Take That', 'Tammi Terrell', 'Tangerine Dream', 'Taylor Swift',
           'Tears For Fears',
           'Teena Marie', 'Temple Of The Dog', 'The Temptations', 'Tesla', 'Texas', 'Thelma Houston', 'Thelonious Monk',
           'Thin Lizzy', 'Thomas Rhett', 'Three Dog Night', 'Tim McGraw', 'Toby Keith', 'Tom Jones', 'Tom Petty',
           'Tom Waits', 'Toots & The Maytals', 'Tori Amos', 'Traffic', 'Traveling Wilburys', 'The Tubes', 'U2', 'UB40',
           'Ultravox', 'Underworld', 'Van der Graaf Generator', 'Vangelis', 'The Velvet Underground', 'The Verve',
           'Vince Gill', 'The Walker Brothers', 'Weezer', 'Wes Montgomery', 'Wet Wet Wet', 'will.i.am', 'Whitesnake',
           'The Who', 'William Orbit', 'Willie Nelson', 'Wilson Pickett', 'Wishbone Ash', 'Wolfmother',
           'Yeah Yeah Yeahs',
           'Yello', 'Yes', 'Zucchero']

Locations = ['Град Event-Hall', 'ЛДС "Юбилейный"',
             'Зеленый театр', 'Palazzo',
             'Воронежская Филармония', 'Воронежский концертный зал']

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

    # for n in range(555):
    #     Artist.query.get(n + 1).artist_name = artists[n]
    #     if n % 10 == 0:
    #         db.session.commit()
    #
    # db.session.commit()
    # n + 1

    ar = Concert.query.all()

    # ar = concert_schema.dump(ar)
    # if len(all_concert) == 0:
    # abort(404)
    return jsonify(json_list=[concert_schema.dump(i) for i in ar])


print(len(artists))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)
