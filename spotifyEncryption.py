from lyricsgenius import Genius

genius = Genius("ytTQBFpeW9m1wOxySiu-h1mIJ_0qiv2E52oRSqoYR8NV5wE9Xka-Ngh2ugLUU88y")
artist = genius.search_artist("Chappell Roan", max_songs=10, include_features=False)
print(artist.songs)

song = artist.song("Casual")
print(song.lyrics)