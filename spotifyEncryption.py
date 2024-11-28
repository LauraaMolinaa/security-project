"""Here's the example from spotipy https://github.com/spotipy-dev/spotipy?tab=readme-ov-file#quick-start"""
from spotapi import Song

song = Song()
gen = song.paginate_songs("weezer")

# # Paginates 100 songs at a time till there's no more
# for batch in gen:
#     for idx, item in enumerate(batch):
#         print(idx, item['item']['data']['name'])
    
# ^ ONLY 6 LINES OF CODE

# Alternatively, you can query a specfic amount
songs = song.query_songs("weezer", limit=20)
data = songs["data"]["searchV2"]["tracksV2"]["items"]
for idx, item in enumerate(data):
    print(idx+1, item['item']['data']['name'])