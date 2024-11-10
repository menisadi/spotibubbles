import pylast
from tqdm import tqdm
import datetime
import json


with open("tokens.json", "r") as file:
    tokens = json.load(file)

password_hash = pylast.md5(tokens.get("last_password"))

# Authenticate
network = pylast.LastFMNetwork(
    api_key=tokens.get("last_api_key"),
    api_secret=tokens.get("last_secret"),
    username=tokens.get("last_username"),
    password_hash=password_hash,
)


def get_latest_album_release_year(artist_name, limit=20):
    try:
        artist = network.get_artist(artist_name)
        albums = artist.get_top_albums(limit=limit)

        # If there are no albums found
        if not albums:
            print(f"No albums found for {artist_name}.")
            return None

        # Retrieve the latest release year by checking each album
        latest_year = None
        last_album = None
        for album_item in tqdm(albums):
            album = album_item.item
            try:
                # FIX: this is not the correct way. The publlished date is not the correct one
                release_date = album.get_wiki("published")
                if release_date:
                    # parse the release date
                    release_date = datetime.datetime.strptime(
                        release_date, "%d %b %Y, %H:%M"
                    )
                    year = int(release_date.year)
                    if latest_year is None or year > latest_year:
                        latest_year = year
                        last_album = album.get_name()
            except:
                continue

        return last_album, latest_year

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


# Example usage
artist_name = "Taylor Swift"
album_name, latest_year = get_latest_album_release_year(artist_name)
if latest_year:
    print(
        f"The latest album ({album_name}) release year for {artist_name} is {latest_year}."
    )
else:
    print("No release year found.")
