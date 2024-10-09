import pylast
import json

with open("tokens.json", "r") as file:
    tokens = json.load(file)

password_hash = pylast.md5(tokens.get("last_password"))

last = pylast.LastFMNetwork(
    api_key=tokens.get("last_api_key"),
    api_secret=tokens.get("last_secret"),
    username=tokens.get("last_username"),
    password_hash=password_hash,
)

my_user = last.get_user(tokens.get("last_username"))

# TODO: we will use lastfm for playcount and spotify for the images
