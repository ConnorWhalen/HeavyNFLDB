from itertools import chain
import os

from flask import Blueprint, Flask, jsonify, render_template, request, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import min

from server import db
from server.models import AlbumArtist, Song, Artist, Album, Link, Video

main_api = Blueprint('main_api', __name__)

@main_api.route("/")
def main_page():
    current_app.logger.info("Loading index.")
    return render_template("index.html")

@main_api.route("/table")
def table():
    current_app.logger.info("Fetching table.")
    return render_template("table.html")

@main_api.route("/album/<int:album_id>")
def album_page(album_id):
    current_app.logger.info("Fetching album %s.", album_id)
    album = Album.query.filter_by(id=album_id).options(
        joinedload(Album.artists),
        joinedload(Album.songs).joinedload(Song.video)
    ).one()

    for song in album.songs:
        song.video.url = song.video.url.replace("watch?v=", "embed/")

    links = (
        db.session.query(Link.site, Link.url)
        .join(Song, Link.song_id == Song.id)
        .filter(Song.album_id == album_id)
        .distinct()
        .order_by(Link.site, Link.url)
        .all()
    )

    first_video = (
        Video.query
        .join(Song, Song.video_id == Video.id)
        .join(Album, Song.album_id == Album.id)
        .filter(Album.id == album_id)
        .first()
    )
    return render_template("album.html", album=album, links=links, thumbnail=first_video.thumbnail_url.replace("default.jpg", "hqdefault.jpg"))

@main_api.route("/artist/<int:artist_id>")
def artist_page(artist_id):
    current_app.logger.info("Fetching artist %s.", artist_id)
    artist = Artist.query.filter_by(id=artist_id).options(
        joinedload(Artist.albums)
    ).one()

    links = (
        db.session.query(Link.site, Link.url)
        .join(Song, Link.song_id == Song.id)
        .filter(Song.artist_id == artist_id)
        .distinct()
        .order_by(Link.site, Link.url)
        .all()
    )

    album_thumbnails = (
        db.session.query(Album.id, min(Video.thumbnail_url))
        .join(AlbumArtist, AlbumArtist.album_id == Album.id)
        .join(Artist, AlbumArtist.artist_id == Artist.id)
        .join(Song, Song.album_id == Album.id)
        .join(Video, Song.video_id == Video.id)
        .filter(Artist.id == artist_id)
        .group_by(Album.id)
        .all()
    )
    thumbnail_map = {album_id: thumbnail_url for album_id, thumbnail_url in album_thumbnails}

    return render_template("artist.html", artist=artist, links=links, thumbnail_map=thumbnail_map)

@main_api.route("/api/songs")
def get_songs():
    current_app.logger.info("Fetching songs.")
    page_number = int(request.args.get("start")) if request.args.get("start") else 0
    page_size = int(request.args.get("length")) if request.args.get("length") else 10

    query = Song.query.options(joinedload(Song.video))

    # Global search:
    # search[value]=&
    # search[regex]=false
    if global_search_value := request.args.get("search[value]"):
        query = Song.filter_global(query, global_search_value)

    # Column info:
    # columns[0][data]=title&
    # columns[0][name]=&
    # columns[0][searchable]=true&
    # columns[0][orderable]=true&
    # columns[0][search][value]=&
    # columns[0][search][regex]=false
    i = 0
    column_names = []
    while column_name := request.args.get(f"columns[{i}][data]"):
        column_names.append(column_name)
        searchable = request.args.get(f"columns[{i}][searchable]") == "true"
        search_value = request.args.get(f"columns[{i}][search][value]") or ""

        if searchable and search_value:
            query = Song.filter_column(query, column_name, search_value)

        i += 1
    
    # Sorting
    # order[0][column]=0&
    # order[0][dir]=asc&
    # order[0][name]
    i = 0
    while sort_index := request.args.get(f"order[{i}][column]"):
        column_name = column_names[int(sort_index)]
        is_asc = request.args.get(f"order[{i}][dir]") == "asc"
        query = Song.sort(query, column_name, is_asc)
    
        i += 1
    
    # Sort by newest by default
    if i == 0:
        query = Song.sort(query, "release_date", False)

    # Increments each call in session
    # draw=1

    # Current local time
    # _=1725403948133

    songs = query.offset(page_number).limit(page_size).all()
    return jsonify({
        "data": [song.to_dict() for song in songs],
        "recordsTotal": Song.query.count(),
        "recordsFiltered": query.count(),
        "draw": int(request.args.get("draw")) if request.args.get("draw") else 0
    })
