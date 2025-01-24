import sqlite3

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()


# Video table
table_check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='video';")

# Duration was created as TEXT. Update to INT
if len(table_check.fetchall()) == 0:
    print("Creating video table")
    cursor.execute(
    """CREATE TABLE video (
        id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        upload_date TEXT,
        duration_secs INT,
        type TEXT,
        thumbnail_url TEXT,
        url TEXT
    );"""
    )
else:
    print("Skipping video table creation")


# Artist table
table_check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artist';")

if len(table_check.fetchall()) == 0:
    print("Creating artist table")
    cursor.execute(
    """CREATE TABLE artist (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT
    );"""
    )
else:
    print("Skipping artist table creation")


# Album table
table_check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='album';")

if len(table_check.fetchall()) == 0:
    print("Creating album table")
    cursor.execute(
    """CREATE TABLE album (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT
    );"""
    )
else:
    print("Skipping album table creation")


# Artist-Album association table
table_check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='album_artist';")

if len(table_check.fetchall()) == 0:
    print("Creating association table")
    cursor.execute(
    """CREATE TABLE album_artist (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        artist_id INTEGER,
        album_id INTEGER,
        FOREIGN KEY(artist_id) REFERENCES artist(id),
        FOREIGN KEY(album_id) REFERENCES album(id)
    );"""
    )
else:
    print("Skipping association table creation")


# Song table
table_check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='song';")

if len(table_check.fetchall()) == 0:
    print("Creating song table")
    cursor.execute(
    """CREATE TABLE song (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        video_id TEXT,
        title TEXT,
        artist TEXT,
        artist_id INTEGER,
        album TEXT,
        album_id INTEGER,
        hometown TEXT,
        release_date TEXT,
        sort_date TEXT,
        genre TEXT,
        label TEXT,
        FOREIGN KEY(video_id) REFERENCES video(id),
        FOREIGN KEY(artist_id) REFERENCES artist(id),
        FOREIGN KEY(album_id) REFERENCES album(id)
    );"""
    )
else:
    print("Skipping song table creation")


# Link table
table_check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='link';")

if len(table_check.fetchall()) == 0:
    print("Creating link table")
    cursor.execute(
    """CREATE TABLE link (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        song_id TEXT,
        site TEXT,
        url TEXT,
        FOREIGN KEY(song_id) REFERENCES song(id)
    );"""
    )
else:
    print("Skipping link table creation")
