import json
import sqlite3

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()

songs = cursor.execute("""
SELECT id, title, artist, album, hometown, release_date, genre, label
FROM song;
""").fetchall()

for i, song in enumerate(songs):
    if i % 100 == 0:
        print(f"Checking {i} of {len(songs)}")
    title =        song[1] if song[1] != "" else None
    artist =       song[2] if song[2] != "" else None
    album =        song[3] if song[3] != "" else None
    hometown =     song[4] if song[4] != "" else None
    release_date = song[5] if song[5] != "" else None
    genre =        song[6] if song[6] != "" else None
    label =        song[7] if song[7] != "" else None
    
    if (    title is None or
            artist is None or
            album is None or
            hometown is None or
            release_date is None or
            label is None
        ):
        cursor.execute(
            """UPDATE song SET
                title = ?,
                artist = ?,
                album = ?,
                hometown = ?,
                release_date = ?,
                genre = ?,
                label = ?
            WHERE id = ?
            """,
            (
                title,
                artist,
                album,
                hometown,
                release_date,
                genre,
                label,
                song[0]
            )
        )

connection.commit()

