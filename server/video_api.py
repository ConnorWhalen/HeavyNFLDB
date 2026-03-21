
from flask import Blueprint, jsonify, render_template, request, current_app

from server.models import Song, Video

video_api = Blueprint('video_api', __name__)

@video_api.route("/")
def main_page():
    current_app.logger.info("Loading videos index.")
    return render_template("videos/index.html")

@video_api.route("/api/videos")
def get_songs():
    current_app.logger.info("Fetching videos.")
    page_number = int(request.args.get("start")) if request.args.get("start") else 0
    page_size = int(request.args.get("length")) if request.args.get("length") else 10

    query = Video.query

    query = query.outerjoin(Song, Song.video_id == Video.id).filter(Song.id.is_(None))

    # Global search:
    # search[value]=&
    # search[regex]=false
    if global_search_value := request.args.get("search[value]"):
        query = Video.filter_global(query, global_search_value)

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
            query = Video.filter_column(query, column_name, search_value)

        i += 1
    
    # Sorting
    # order[0][column]=0&
    # order[0][dir]=asc&
    # order[0][name]
    i = 0
    while sort_index := request.args.get(f"order[{i}][column]"):
        column_name = column_names[int(sort_index)]
        is_asc = request.args.get(f"order[{i}][dir]") == "asc"
        query = Video.sort(query, column_name, is_asc)
    
        i += 1
    
    # Sort by newest by default
    if i == 0:
        query = Video.sort(query, "upload_date", False)

    # Increments each call in session
    # draw=1

    # Current local time
    # _=1725403948133

    videos = query.offset(page_number).limit(page_size).all()
    return jsonify({
        "data": [video.to_dict() for video in videos],
        "recordsTotal": Video.query.count(),
        "recordsFiltered": query.count(),
        "draw": int(request.args.get("draw")) if request.args.get("draw") else 0
    })
