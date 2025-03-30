from sqlalchemy import nullslast, or_
from sqlalchemy.orm import Query

from server import db

class Video(db.Model):
    id = db.Column(db.Text(), primary_key=True)
    title = db.Column(db.Text())
    description = db.Column(db.Text())
    upload_date = db.Column(db.Text())
    duration_secs = db.Column(db.Integer())
    type = db.Column(db.Text())
    thumbnail_url = db.Column(db.Text())
    url = db.Column(db.Text())

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
    

class Artist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())
    albums = db.relationship("Album", secondary="album_artist", back_populates="artists")
    songs = db.relationship("Song", back_populates="artist_rel")
    

class Album(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())
    artists = db.relationship("Artist", secondary="album_artist", back_populates="albums")
    songs = db.relationship("Song", back_populates="album_rel")
    

class AlbumArtist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    artist_id = db.Column(db.Integer(), db.ForeignKey("artist.id"))
    album_id = db.Column(db.Integer(), db.ForeignKey("album.id"))


class Song(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    video_id = db.Column(db.Text(), db.ForeignKey("video.id"))
    video = db.relationship("Video", foreign_keys=[video_id])
    title = db.Column(db.Text())
    artist = db.Column(db.Text())
    artist_id = db.Column(db.Integer(), db.ForeignKey("artist.id"))
    artist_rel = db.relationship("Artist", foreign_keys=[artist_id])
    album = db.Column(db.Text())
    album_id = db.Column(db.Integer(), db.ForeignKey("album.id"))
    album_rel = db.relationship("Album", foreign_keys=[album_id], back_populates="songs")
    hometown = db.Column(db.Text())
    # Release date as logged on YT
    release_date = db.Column(db.Text())
    # Precise date used for sorting
    sort_date = db.Column(db.Text())
    genre = db.Column(db.Text())
    label = db.Column(db.Text())
    links = db.relationship("Link", back_populates="song")

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
            "genre": self.genre,
            "label": self.label,
            # Make URL embed-compatible
            "video_url": self.video.url.replace("watch?v=", "embed/")
        }
    
    @classmethod
    def filter_global(cls, query: Query, value: str) -> Query:
        return query.filter(
            or_(
                Song.title.contains(value),
                Song.artist.contains(value),
                Song.album.contains(value),
                Song.hometown.contains(value),
                Song.release_date.contains(value),
                Song.genre.contains(value),
                Song.label.contains(value),
            )
        )
    
    @classmethod
    def filter_column(cls, query: Query, filter_name: str, filter_value: str) -> Query:
        column = None
        match filter_name:
            case "title":
                column = Song.title
            case "artist":
                column = Song.artist
            case "album":
                column = Song.album
            case "hometown":
                column = Song.hometown
            case "release_date":
                column = Song.release_date
            case "genre":
                column = Song.genre
            case "label":
                column = Song.label
        
        if column:
            query = query.filter(column.contains(filter_value))
        
        return query

    @classmethod
    def sort(cls, query: Query, sort_name: str, is_asc: bool) -> Query:
        column = None
        match sort_name:
            case "title":
                column = Song.title
            case "artist":
                column = Song.artist
            case "album":
                column = Song.album
            case "hometown":
                column = Song.hometown
            case "release_date":
                column = Song.sort_date
            case "genre":
                column = Song.genre
            case "label":
                column = Song.label
        
        if column:
            query = query.order_by(nullslast(column.asc() if is_asc else column.desc()))
        
        return query


class Link(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    song_id = db.Column(db.Text(), db.ForeignKey("song.id"))
    song = db.relationship("Song", foreign_keys=[song_id], back_populates="links")
    site = db.Column(db.Text())
    url = db.Column(db.Text())

    def to_dict(self):
        return {
            "id": self.id,
            "song_id": self.song_id,
            "site": self.site,
            "url": self.url,
        }
