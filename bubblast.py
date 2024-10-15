import pylast
import json
import matplotlib.pyplot as plt


def fix_name(name):
    """Reverse the name, by letter, if it is not ascii"""
    if name.isascii():
        return name
    else:
        return name[::-1]


def fix_name2(name):
    """Reverse the name, by word, if it is not ascii"""
    if name.isascii():
        return name
    else:
        return " ".join(name.split(" ")[::-1])


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
total_plays = my_user.get_playcount()

# create a list of artists - names and counts
limit_top = 15
art_list = my_user.get_top_artists(period="PERIOD_OVERALL", limit=limit_top)
artists_list = [a.item.name for a in art_list]
artists_counts = [int(a.weight) for a in art_list]
artists_list_fixed = [fix_name2(a) for a in artists_list]

# rest_of_play = total_plays - sum(artists_counts)
# artists_list.append("Other")
# artists_counts.append(rest_of_play)

combined_list = list(zip(artists_list_fixed, artists_counts))

for a in combined_list:
    print(f"{a[0]}: {a[1]}")

# Fix artists with Hebrew names (which name is being displayed backwards on the chart)
# artists_list = [fix_name(a) for a in artists_list]

# plot the top artists as a bar chart
# plt.bar(artists_list, artists_counts)
# plt.xticks(rotation=90)
# plt.show()


# TODO: we will use lastfm for playcount and spotify for the images
