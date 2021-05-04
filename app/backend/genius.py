import requests
import json
from genius_key import headers

baseUrl = 'https://api.genius.com'


def getting_artist_info(id: str):
    path = 'artists/'
    request_uri = '/'.join([baseUrl, path])
    new_req = request_uri + str(id)
    r = requests.get(new_req, headers=headers)
    arti = r.json()
    return arti["response"]["artist"]["description"]


def getting_artist_id(songname: str):
    searchUrl = baseUrl + "/search"
    songTitle = songname
    data = {'q': songTitle}
    response = requests.get(searchUrl, params=data, headers=headers)
    jason = response.json()
    return jason["response"]["hits"][0]["result"]["primary_artist"]["id"]


def main():
    songTitle = "Fack"
    id = getting_artist_id(songTitle)
    info = getting_artist_info(id)
    print(info)


if __name__ == '__main__':
    main()