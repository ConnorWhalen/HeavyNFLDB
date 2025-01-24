import json
import sqlite3
from textwrap import dedent

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()

# Populate videos
video_ids = cursor.execute("SELECT id FROM video;").fetchall()
video_ids = [video_id[0] for video_id in video_ids]

with open("videos-typed.json") as f:
    videos = json.loads(f.read())

new_videos = [video for video in videos if video["id"] not in video_ids]
print(f"Inserting {len(new_videos)} videos")

for i, video in enumerate(new_videos):
    print(f"Inserting {i} of {len(new_videos)}")

    duration_raw = video["duration"]

    hours = 0
    if 'H' in duration_raw:
        hours, duration_raw = duration_raw.split('H')
        hours = int(hours)
    
    minutes = 0
    if 'M' in duration_raw:
        minutes, duration_raw = duration_raw.split('M')
        minutes = int(minutes)
    
    seconds = 0
    if 'S' in duration_raw:
        seconds, duration_raw = duration_raw.split('S')
        seconds = int(seconds)


    insert_statement = dedent(f"""INSERT INTO video VALUES (
        '{video["id"]}',
        '{video["title"].replace('\'', '\'\'')}',
        '{video["description"].replace('\'', '\'\'')}',
        '{video["upload_date"]}',
        {hours * 3600 + minutes * 60 + seconds},
        '{video["type"]}',
        '{video["thumbnail"]["url"]}',
        'https://www.youtube.com/watch?v={video["id"]}'
    )""")
    cursor.execute(insert_statement)

connection.commit()

# Populate Songs
videos = cursor.execute("SELECT id, title, description FROM video WHERE type='song';").fetchall()

song_video_ids = cursor.execute("SELECT video_id FROM song;").fetchall()
song_video_ids = [video_id[0] for video_id in song_video_ids]

new_song_videos = [video for video in videos if video[0] not in song_video_ids]
print(f"Inserting {len(new_song_videos)} songs")

for i, video in enumerate(new_song_videos):
    if i % 100 == 0:
        print(f"Processing {i+1} of {len(new_song_videos)}")

    video_id, video_title, video_description = video

    title = ""
    artist = ""
    album = ""
    hometown = ""
    release_date = ""
    genre = ""
    label = ""
    links = []

    video_title = video_title.replace('--', '-')
    title_artist, title = video_title.split(' - ', 1)
    title_artist = title_artist.strip()
    title = title.strip(" \"")
    
    for line in video_description.splitlines():
        if ":" in line and " is:" not in line:
            key, value = line.split(':', 1)

            match key:
                case "Artist" | "Aritst":
                    description_artist = value.strip()
                    if title_artist != description_artist:
                        print(f"ARTIST NAME MISMATCH! {title_artist} {description_artist}")
                    
                    if description_artist in ["MIstwalker", "Bongwater 666 [aka Bongwater]", "Beereaucracy / Catshit", "Jon Free and Neddal Ayad"]:
                        artist = title_artist
                    else:
                        artist = description_artist
                
                case "Album":
                    album = value.strip()
                case "Hometown":
                    hometown = value.strip()
                case "Release Date":
                    if "Unknown" not in value:
                        release_date = value.strip()
                case "Year":
                    if "Unknown" not in value:
                        release_date = value.strip()
                case "Genre":
                    genre = value.strip()
                case "Label":
                    label = value.strip()

                case "Instagram" | "Reddit" | "Reddit Download" | "Twitter" | "Bandcamp" | "Unsigned" | "Website" | "Blogger" | "Metal Archives" | "YouTube" | "Linktree" | "TikTok" | "Apple Music" | "Wordpress" | "MySpace" | "Tumblr" | "Facebook" | "ReverbNation" | "SoundCloud":
                    links.append([key.strip(), value.strip()])
                case "Download":
                    links.append(["Reddit Download", value.strip()])
                case "Greg R. Sweetapple - All InstrumentsBandcamp" | "Purchase":
                    links.append(["Bandcamp", value.strip()])
                case "Facebook Fan Page" | "Fan Club":
                    links.append(["Facebook Group", value.strip()])
                case "Soundcloud":
                    links.append(["SoundCloud", value.strip()])
                case "Listen":
                    if "soundcloud" in value:
                        links.append(["SoundCloud", value.strip()])
                    elif "reverbnation" in value:
                        links.append(["ReverbNation", value.strip()])
                
                case "Note" | "PLEASE NOTE":
                    title = value.split("\"")[1]


    insert_statement = dedent(f"""INSERT INTO song (
        video_id,
        title,
        artist,
        album,
        hometown,
        release_date,
        genre,
        label
    )
    VALUES (
        '{video_id}',
        '{title.replace('\'', '\'\'')}',
        '{artist.replace('\'', '\'\'')}',
        '{album.replace('\'', '\'\'')}',
        '{hometown.replace('\'', '\'\'')}',
        '{release_date.replace('\'', '\'\'')}',
        '{genre.replace('\'', '\'\'')}',
        '{label.replace('\'', '\'\'')}'
    ) RETURNING id""")

    # print(insert_statement)
    cursor.execute(insert_statement)
    song_id = cursor.lastrowid
    
    # throw away song id to unblock connection
    if len(links) == 0:
        cursor.fetchall()

    for link in links:
        insert_statement = dedent(f"""INSERT INTO link (
            song_id,
            site,
            url
        )
        VALUES (
            '{song_id}',
            '{link[0]}',
            '{link[1].strip('\'')}'
        )""")

        cursor.execute(insert_statement)

    connection.commit()
