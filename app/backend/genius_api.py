import requests
# import json
from genius_key import headers

baseUrl = 'https://api.genius.com'

class Genius:
    def get_artist_info_by_id(self, id):
        path = 'artists/'
        request_uri = '/'.join([baseUrl, path])
        new_req = request_uri + str(id) + '?text_format=html'
        r = requests.get(new_req, headers=headers)
        arti = r.json()
        if r.status_code != 200:
            return []
        return arti["response"]["artist"]["description"]

    def get_artist_id_by_songname(self, songname: str):
        searchUrl = baseUrl + "/search"
        songTitle = songname
        data = {'q': songTitle}
        response = requests.get(searchUrl, params=data, headers=headers)
        jason = response.json()
        return jason["response"]["hits"][0]["result"]["primary_artist"]["id"]

    def get_artist_id_by_name(self, name: str):
        searchUrl = baseUrl + "/search"
        songTitle = name
        data = {'q': name}
        response = requests.get(searchUrl, params=data, headers=headers)
        jason = response.json()

        for hit in jason["response"]["hits"]:
            if hit["result"]["primary_artist"]['name'] == name:
                return hit["result"]["primary_artist"]['id']
        return 0
