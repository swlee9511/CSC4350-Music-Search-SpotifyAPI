import requests
import base64
import os
from dotenv import find_dotenv, load_dotenv
from random import randint

# Authentication process
load_dotenv(find_dotenv())
AUTH_URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

r = requests.post(
    AUTH_URL,
    {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    },
)
# token obtained
token = r.json()["access_token"]
headers = {
    "Authorization": "Bearer {token}".format(token=token),
}

# Hard coded ids of my favorite artists
tame_impala_id = "5INjqkS1o8h1imAzPqGZBb"
chatmonchy_id = "0GtBUVp1cWdIUKwm2GHTHc"
drake_id = "3TVXtAsR1Inumwj472S9r4"
id_arr = [tame_impala_id, chatmonchy_id, drake_id]


def get_song_data(id):
    # choose randomly
    # id = id_arr[randint(0,2)]

    BASE_URL = f"https://api.spotify.com/v1/artists/{id}/top-tracks"
    params = {"market": "US"}

    r = requests.get(BASE_URL, headers=headers, params=params)
    r = r.json()

    def get_song_name(r):
        return r["tracks"][0]["name"]

    def get_song_artist(r):
        return r["tracks"][0]["album"]["artists"][0]["name"]

    def get_song_image(r):
        return r["tracks"][0]["album"]["images"][0]["url"]

    def get_song_preview(r):
        return r["tracks"][0]["preview_url"]

    song_name = get_song_name(r)
    artist_name = get_song_artist(r)
    song_image = get_song_image(r)
    song_preview = get_song_preview(r)

    return {
        "song_name": song_name,
        "artist_name": artist_name,
        "song_image": song_image,
        "song_preview": song_preview,
    }


def search_artist(user_input):
    if user_input == None or user_input == "":
        return "-1"
    else:
        SEARCH_URL = "https://api.spotify.com/v1/search"
        params = {"q": user_input, "type": "artist"}
        r = requests.get(SEARCH_URL, headers=headers, params=params)
        r = r.json()
        artist_data = r["artists"]["items"][0]

        if artist_data["name"] == user_input:
            artist_id = artist_data["id"]
        else:
            artist_id = "-1"
        return artist_id


# data = get_song_data()
#
# try:
#    print(data['song_name'])
#    print(data['artist_name'])
#    print(data['song_image'])
#    print(data['song_preview'])
# except KeyError:
#    print("Couldn't fetch New Releases!!!")
