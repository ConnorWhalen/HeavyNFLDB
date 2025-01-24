from calendar import month
from datetime import date, datetime
import json
import sqlite3
from textwrap import dedent
from time import strptime

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()

song2s = cursor.execute("""
SELECT * song2;
""").fetchall()

if len(song2s) != 0:
    print("Skipping song-song2 copy")
else:
    songs = cursor.execute("""
    SELECT id, video_id, title, artist, album, hometown, release_date, genre, label, sort_date
    FROM song;
    """).fetchall()

    for song in songs:
        insert_statement = cursor.execute(
            dedent(f"""INSERT INTO song2 (
                id,
                video_id,
                title,
                artist,
                album,
                hometown,
                release_date,
                genre,
                label,
                sort_date
            )
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            );"""),
            (
                song[0],
                song[1],
                song[2],
                song[3],
                song[4],
                song[5],
                song[6],
                song[7],
                song[8],
                song[9],
            )
        )
    
    print("Songs copied")


link2s = cursor.execute("""
SELECT * link2;
""").fetchall()

if len(link2s) != 0:
    print("Skipping link-link2 copy")
else:
    links = cursor.execute("""
    SELECT id, song_id, site, url
    FROM link;
    """).fetchall()

    for link in links:
        cursor.execute(
            dedent(f"""INSERT INTO link2 (
                id,
                song_id,
                site,
                url
            )
            VALUES (
                ?,
                ?,
                ?,
                ?
            );"""),
            (
                link[0],
                link[1],
                link[2],
                link[3],
            )
    )
        
    print("Links copied")

connection.commit()