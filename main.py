import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open("tokens.json", "r") as file:
    tokens = json.load(file)

scope = "user-top-read user-read-recently-played"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=tokens.get("client_id"),
        client_secret=tokens.get("client_secret"),
        redirect_uri=tokens.get("redirect_uri"),
    )
)

# get the top artists for the user
top_artists = sp.current_user_top_artists(limit=20)
print(top_artists)
# And now the amount of times they were played
# TODO: find a way
