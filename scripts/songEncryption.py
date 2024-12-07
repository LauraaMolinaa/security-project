import random
from lyricsgenius import Genius

nbr = random.randint(1, 249990)
print(nbr)

genius = Genius("ytTQBFpeW9m1wOxySiu-h1mIJ_0qiv2E52oRSqoYR8NV5wE9Xka-Ngh2ugLUU88y")
#artist = genius.search_artist("Chappell Roan", max_songs=10, include_features=False)
#print(artist.songs)

song = genius.search_song(song_id=nbr)

print(song.title)
print(song.artist)
print(song.lyrics)

#Encryption
