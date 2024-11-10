import json
import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime


def fix_name(name):
    """Reverse the name, by word, if it is not ascii"""
    if name.isascii():
        return name
    else:
        return " ".join(name.split(" ")[::-1])


def get_top_artists(sp, term="long_term", limit=20):
    top_artists = sp.current_user_top_artists(limit=limit, time_range=term)

    return top_artists


def get_albums_by_year(sp, artist_id, year=2024):
    albums = sp.artist_albums(artist_id, limit=5)
    # filter albums by release year
    albums = [
        album
        for album in albums["items"]
        if int(album["release_date"].split("-")[0]) == year
    ]

    return albums


def did_release_album_this_year(sp, artist_id):
    current_year = datetime.datetime.now().year

    albums = get_albums_by_year(sp, artist_id, current_year)

    for album in albums:
        if album["album_type"] == "album" and "edition" not in album["name"].lower():
            return album["name"]

    return None


def main(term, limit):
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

    top_artists = get_top_artists(sp, term=term, limit=limit)

    for i, artist in enumerate(top_artists["items"]):
        if did_release_album_this_year(sp, artist["id"]):
            current_year = datetime.datetime.now().year
            album_from_this_year = get_albums_by_year(
                sp, artist["id"], year=current_year
            )
            print(
                f"{i}: {fix_name(artist['name'])} - {fix_name(album_from_this_year[0]['name'])}"
            )


if __name__ == "__main__":
    # parse the parameter : "time_range"" and "limit"
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_range", type=str, default="long_term")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    # help
    if args.time_range not in ["short_term", "medium_term", "long_term"]:
        # try to convert "short" to "short_term" etc.
        attemted_fix_time_range = args.time_range.lower() + "_term"
        if attemted_fix_time_range in [
            "short_term",
            "medium_term",
            "long_term",
        ]:
            args.time_range = attemted_fix_time_range
        else:
            print("time_range must be one of: short_term, medium_term, long_term")
            exit(1)

    if args.limit < 1:
        print("limit must be at least 1")
        exit(1)

    main(args.time_range, args.limit)
