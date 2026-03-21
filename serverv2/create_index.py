import gzip
import json

from lunr import lunr
from sqlalchemy import BinaryExpression
from sqlalchemy.orm import Session, joinedload

from serverv2 import engine
from serverv2.models import Base, Video, Artist, Album, AlbumArtist, Song, Link


def create_index(objs: Base, model: type[Base], name: str, idx_fields: list[str]):
    print(f"Found {len(objs)} {model.__name__}")

    obj_dict = [obj.to_dict() for obj in objs]

    obj_idx = lunr(
        ref="id",
        fields=idx_fields,
        documents=obj_dict
    )

    with gzip.open(f"serverv2/static/data/{name}.json.gz", "wt") as f:
        json.dump(obj_dict, f)

    with gzip.open(f"serverv2/static/data/{name}_idx.json.gz", "wt") as f:
        json.dump(obj_idx.serialize(), f)


def save_model(session: Session, model: type[Base], name: str, filters: list[BinaryExpression] | None = None):
    query = session.query(model)
    if filters:
        query = query.filter(*filters)

    objs = query.all()

    print(f"Found {len(objs)} {model.__name__}")

    obj_dict = [obj.to_dict() for obj in objs]

    with gzip.open(f"serverv2/static/data/{name}.json.gz", "wt") as f:
        json.dump(obj_dict, f)


def create_indexes():
    with Session(engine) as session:
        create_index(
            session.query(Song).all(),
            Song,
            "song",
            idx_fields=[
                "title",
                "artist",
                "album",
                "hometown",
                "release_date",
                "sort_date",
                "genre",
                "label"
            ]
        )

        create_index(
            session.query(Video).filter(Video.type != "song").all(),
            Video,
            "video",
            idx_fields=[
                "title",
                "description",
                "upload_date",
            ]
        )

        create_index(
            session.query(Album).options(joinedload(Album.artists), joinedload(Album.songs)).all(),
            Album,
            "album",
            idx_fields=[
                "name",
                "artists",
                "songs"
            ]
        )

        create_index(
            session.query(Artist).options(joinedload(Artist.songs)).all(),
            Artist,
            "artist",
            idx_fields=[
                "name",
                "hometowns",
                "genres",
                "albums"
            ]
        )

        save_model(session, AlbumArtist, 'album_artist')
        save_model(session, Link, 'link')
