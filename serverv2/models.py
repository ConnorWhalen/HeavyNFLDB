import sqlalchemy as sa
from sqlalchemy import desc, nullslast, or_, text
from sqlalchemy.orm import DeclarativeBase, Query, relationship


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = 'video'

    id = sa.Column(sa.Text(), primary_key=True)
    title = sa.Column(sa.Text())
    description = sa.Column(sa.Text())
    upload_date = sa.Column(sa.Text())
    duration_secs = sa.Column(sa.Integer())
    type = sa.Column(sa.Text())
    thumbnail_url = sa.Column(sa.Text())
    url = sa.Column(sa.Text())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "upload_date": self.upload_date,
            "duration_secs": self.duration_secs,
            "type": self.type,
            "thumbnail_url": self.thumbnail_url,
            "url": self.url.replace("watch?v=", "embed/"),
        }
    

class Artist(Base):
    __tablename__ = 'artist'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.Text())
    albums = relationship("Album", secondary="album_artist", back_populates="artists")
    songs = relationship("Song", back_populates="artist_rel", order_by=desc(text("sort_date")))

    def to_dict(self):
        all_genres = {song.genre for song in self.songs if song.genre}
        genres = []
        for entry in all_genres:
            for g in entry.split('/'):
                g = g.strip()
                if g not in genres:
                    genres.append(g)

        return {
            "id": self.id,
            "name": self.name,
            "hometowns": list({song.hometown for song in self.songs if song.hometown}),
            "genres": genres,
            "albums": [album.name for album in self.albums],
            "album_ids": [album.id for album in self.albums],
            "thumb_video_id": self.songs[0].video_id,
        }
    

class Album(Base):
    __tablename__ = 'album'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.Text())
    artists = relationship("Artist", secondary="album_artist", back_populates="albums")
    songs = relationship("Song", back_populates="album_rel", order_by=desc(text("sort_date")))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "artists": [artist.name for artist in self.artists],
            "artist_ids": [artist.id for artist in self.artists],
            "thumb_video_id": self.songs[0].video_id,
            "songs": [song.title for song in self.songs],
            "song_ids": [song.id for song in self.songs]
        }
    

class AlbumArtist(Base):
    __tablename__ = 'album_artist'

    id = sa.Column(sa.Integer(), primary_key=True)
    artist_id = sa.Column(sa.Integer(), sa.ForeignKey("artist.id"))
    album_id = sa.Column(sa.Integer(), sa.ForeignKey("album.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "artist_id": self.artist_id,
            "album_id": self.album_id
        }


class Song(Base):
    __tablename__ = 'song'
    id = sa.Column(sa.Integer(), primary_key=True)
    video_id = sa.Column(sa.Text(), sa.ForeignKey("video.id"))
    video = relationship("Video", foreign_keys=[video_id])
    title = sa.Column(sa.Text())
    artist = sa.Column(sa.Text())
    artist_id = sa.Column(sa.Integer(), sa.ForeignKey("artist.id"))
    artist_rel = relationship("Artist", foreign_keys=[artist_id])
    album = sa.Column(sa.Text())
    album_id = sa.Column(sa.Integer(), sa.ForeignKey("album.id"))
    album_rel = relationship("Album", foreign_keys=[album_id], back_populates="songs")
    hometown = sa.Column(sa.Text())
    # Release date as logged on YT
    release_date = sa.Column(sa.Text())
    # Precise date used for sorting
    sort_date = sa.Column(sa.Text())
    genre = sa.Column(sa.Text())
    label = sa.Column(sa.Text())
    links = relationship("Link", back_populates="song")

    def to_dict(self):
        return {
            "id": self.id,
            "video_id": self.video_id,
            "title": self.title,
            "artist": self.artist,
            "artist_id": self.artist_id,
            "album": self.album,
            "album_id": self.album_id,
            "hometown": self.hometown,
            "release_date": self.release_date,
            "sort_date": self.sort_date,
            "genre": self.genre,
            "label": self.label,
            # Make URL embed-compatible
            "video_url": self.video.url.replace("watch?v=", "embed/")
        }

class Link(Base):
    __tablename__ = 'link'
    id = sa.Column(sa.Integer(), primary_key=True)
    song_id = sa.Column(sa.Text(), sa.ForeignKey("song.id"))
    song = relationship("Song", foreign_keys=[song_id], back_populates="links")
    site = sa.Column(sa.Text())
    url = sa.Column(sa.Text())

    def to_dict(self):
        return {
            "id": self.id,
            "song_id": self.song_id,
            "site": self.site,
            "url": self.url,
        }
