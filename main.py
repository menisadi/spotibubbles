import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open("tokens.json", "r") as file:
    tokens = json.load(file)

scope = "user-top-read"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=tokens.get("client_id"),
        client_secret=tokens.get("client_secret"),
        redirect_uri=tokens.get("redirect_uri"),
    )
)

results = sp.current_user_top_artists()
print(results)
