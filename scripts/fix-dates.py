from calendar import month
from datetime import date, datetime
import json
import sqlite3
from time import strptime

connection = sqlite3.connect("heavy-nfld.db")

cursor = connection.cursor()

songs = cursor.execute("""
SELECT id, title, artist, album, hometown, release_date, genre, label
FROM song
WHERE release_date IS NOT NULL AND sort_date IS NULL;
""").fetchall()


ones = 0
twos = 0
threes = 0
mores = 0


for i, song in enumerate(songs):
    # if i % 100 == 0:
    #     print(f"Checking {i} of {len(songs)}")
        
    release_date = song[5]
    sort_date = None

    splt = release_date.split(" ")
    if len(splt) == 1:
        # if len(release_date) != 4:
        #     print("ONE PART: " + release_date)
        # else:
        #     x = int(release_date)
        ones += 1
    elif len(splt) == 2:
        # print("TWO PARTS: " + release_date)
        twos += 1
    elif len(splt) == 3:
        # try:
        #     int(splt[1].strip(',thsnrd'))
        # except ValueError:
        #     print("NOT DAY INT: " + release_date)
        
        # if len(splt[2].strip()) != 4:
        #     print("YEAR NOT FOUR: " + release_date)
        # else:
        #     try:
        #         int(splt[2].strip())
        #     except ValueError:
        #         print("YEAR NOT INT: " + release_date)
        threes += 1
    else:
        # print("TOO MANY PARTS: " + str(song[0]) + " " + release_date)
        mores += 1
    

    if release_date == "July 1988 [Original] / June 30th, 2021 [Rerelease]":
        sort_date = date(1988, 7, 1)
    elif release_date == "2009-2011 (2016)":
        sort_date = date(2009, 1, 1)
    elif len(splt) == 2:
        sort_date = datetime.strptime(release_date, "%B %Y").date()
    
    if release_date == "1990's":
        sort_date = date(1990, 1, 1)
    elif release_date == "2009(?)":
        sort_date = date(2009, 1, 1)
    elif release_date == "2006?":
        sort_date = date(2006, 1, 1)
    elif release_date == "2001-2004":
        sort_date = date(2001, 1, 1)
    elif len(splt) == 1:
        sort_date = date(int(release_date), 1, 1)

    if release_date == "1996 (Reissued 2007)":
        sort_date = date(1996, 1, 1)
    elif release_date == "Februrary 3rd, 2020":
        sort_date = date(2020, 2, 3)
    elif len(splt) == 3:
        sort_date = datetime.strptime(
            f"{splt[0]} {splt[1].strip(',thsnrd')} {splt[2].strip()}",
            "%B %d %Y"
        ).date()
    
    
    if sort_date is not None:
        cursor.execute(
            """UPDATE song SET
                sort_date = ?
            WHERE id = ?
            """,
            (
                sort_date.isoformat(),
                song[0]
            )
        )

print("ONES: " + str(ones))
print("TWOS: " + str(twos))
print("THREES: " + str(threes))
print("MORES: " + str(mores))

connection.commit()

