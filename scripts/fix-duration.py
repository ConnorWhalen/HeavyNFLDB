import json
import sqlite3

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()

videos = cursor.execute("SELECT id, title FROM video WHERE type='song';").fetchall()

artists = set()
songs = set()
for i, video in enumerate(videos):
    # print(f"Checking {i} of {len(videos)}")
    title = video[1]

    if ' - ' in title:
        parts = title.split(' - ')
        if len(parts) != 2:
            print(f"TITLE {title} DOES NOT HAVE 2 PARTS")
        artists.add(parts[0])

for artist in artists:
    print(artist)
