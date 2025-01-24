from calendar import month
from collections import defaultdict
from datetime import date, datetime
import json
import sqlite3
from textwrap import dedent
from time import strptime

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()

songs = cursor.execute(
"""
SELECT id,
       title,
       album,
       album_id
FROM song;
""").fetchall()

for song in songs:
    song_id = song[0]
    title = song[1]
    album = song[2]
    album_id = song[3]

    if '"' in title:
        new_title = title.replace('"', '')
        cursor.execute(
            """UPDATE song
            SET title = ?
            WHERE id = ?""", (
                new_title, song_id
            )
        )
    
    if '"' in album:
        new_name = album.replace('"', '')
        cursor.execute(
            """UPDATE song
            SET album = ?
            WHERE id = ?""", (
                new_name, song_id
            )
        )
        cursor.execute(
            """UPDATE album
            SET name = ?
            WHERE id = ?""", (
                new_name, album_id
            )
        )


connection.commit()
