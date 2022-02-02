import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def get_lyrics_url(artist_name):
    ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
    BASE_URL = "http://api.genius.com/search/"

    params = {
        "q": artist_name,
        "access_token": ACCESS_TOKEN,
    }

    r = requests.get(BASE_URL, params=params)
    r = r.json()

    return r["response"]["hits"][0]["result"]["url"]
