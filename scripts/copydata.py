import sqlite3

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()

videos = cursor.execute("SELECT id, title, description, upload_date, duration_secs, type, thumbnail_url, url FROM video;").fetchall()

cursor.executemany(f"""INSERT INTO video2 (id, title, description, upload_date, duration_secs, type, thumbnail_url, url) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?
)""", videos)

connection.commit()
