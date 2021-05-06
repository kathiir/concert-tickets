import requests
import json
from genius_key import headers

baseUrl = 'https://api.genius.com'


class Genius():
    def get_artist_info_by_id(self, id):
        path = 'artists/'
        request_uri = '/'.join([baseUrl, path])
        new_req = request_uri + str(id)
        r = requests.get(new_req, headers=headers)
        arti = r.json()
        return arti["response"]["artist"]["description"]

    def get_artist_id_by_songname(self, songname: str):
        searchUrl = baseUrl + "/search"
        songTitle = songname
        data = {'q': songTitle}
        response = requests.get(searchUrl, params=data, headers=headers)
        jason = response.json()
        return jason["response"]["hits"][0]["result"]["primary_artist"]["id"]
