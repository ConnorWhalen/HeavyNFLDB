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
       video_id,
       title,
       artist,
       album,
       hometown,
       release_date,
       sort_date,
       genre,
       label
FROM song;
""").fetchall()

artists = defaultdict(list)
albums = defaultdict(list)
artist_albums = defaultdict(list)
for song in songs:
    song_id = song[0]
    artist = song[3]
    album = song[4]
    release_date = song[6]

    artist_albums[(artist, album)].append(release_date)
    if artist not in albums[album]:
        albums[album].append(artist)

    # Add artist if needed
    artist_check = cursor.execute(
        """SELECT id
        FROM artist
        WHERE name = ?""", (
            artist,
        )
    ).fetchall()

    if len(artist_check) > 0:
        artist_id = artist_check[0][0]
    else:
        cursor.execute(
            """INSERT INTO artist (name) VALUES (?) RETURNING id
            """, (
                artist,
            )
        )
        artist_id = cursor.lastrowid

        
    # Add album if needed
    album_id = None

    existing_album_check = cursor.execute(
        """SELECT al.id, al.name, ar.id, ar.name, s.release_date
        FROM album al
        INNER JOIN album_artist aa ON aa.album_id = al.id
        INNER JOIN artist ar ON aa.artist_id = ar.id
        INNER JOIN song s ON s.album_id = al.id AND s.artist_id = ar.id
        WHERE al.name = ?
        """, (
            album,
        )
    ).fetchall()

    # Full match
    if full_match := next((
            al_id
            for al_id, al, _, ar, rel in existing_album_check
            if al == album and ar == artist and rel == release_date
        ), None
    ):
        album_id = full_match
    
    # Artist has albums with same name but different release dates
    elif date_mismatch := next((
            al_id
            for al_id, al, _, ar, rel in existing_album_check
            if al == album and ar == artist and rel != release_date
        ), None
    ):
        print(f"DATE MISMATCH {artist} - {album}")
        album_id = None
    
    # Other artists have an album with this name
    elif artist_mismatch := next((
            al_id
            for al_id, al, _, ar, _ in existing_album_check
            if al == album and ar != artist
        ), None
    ):
        if "Demo" not in album and album != "EP":
            album_id = artist_mismatch
            print(f"MERGING ALBUM {artist} - {album}")
            cursor.execute(
                """INSERT INTO album_artist (artist_id, album_id) VALUES (?, ?)
                """, (
                    artist_id,
                    album_id
                )
            )
        else:
            print(f"MAKING SEPARATE ALBUM {artist} - {album}")
    
    if album_id is None:
        cursor.execute(
            """INSERT INTO album (name) VALUES (?) RETURNING id
            """, (
                album,
            )
        )
        album_id = cursor.lastrowid

        cursor.execute(
            """INSERT INTO album_artist (artist_id, album_id) VALUES (?, ?)
            """, (
                artist_id,
                album_id
            )
        )

    
    # Update song
    cursor.execute(
        """UPDATE song
        SET artist_id = ?, album_id = ?
        WHERE id = ?""", (
            artist_id, album_id, song_id
        )
    )

connection.commit()
