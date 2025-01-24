import json

from pyyoutube import Client, Thumbnails

client = Client(api_key=API_KEY)

# resp = client.channels.list(for_handle="@heavynfld", parts=["contentDetails"])

# channel = resp.items[0]

# print(channel.contentDetails.relatedPlaylists.uploads)

resp = client.playlistItems.list(playlist_id=PLAYLIST_ID, parts=["contentDetails"], max_results=50)

videos = []

while len(videos) < resp.pageInfo.totalResults:
    video_ids = []
    print(f"Found {len(resp.items)} playlist items")
    for playlist_item in resp.items:
        video_ids.append((playlist_item.contentDetails.videoId))

    v_resp = client.videos.list(video_id=video_ids, max_results=50)
    print(f"Found {len(v_resp.items)} videos")
    
    for video in v_resp.items:
        videos.append(video)

    page_token = resp.nextPageToken
    resp = client.playlistItems.list(playlist_id=PLAYLIST_ID, parts=["contentDetails"], max_results=50, page_token=page_token)

    print(f"Loaded {len(videos)} of {resp.pageInfo.totalResults}")

videos_json = []
for video in videos:
    videos_json.append({
        "id": video.id,
        "title": video.snippet.title,
        "description": video.snippet.description,
        "upload_date": video.snippet.publishedAt,
        "thumbnail": {
            "url": video.snippet.thumbnails.default.url,
            "width": video.snippet.thumbnails.default.width,
            "height": video.snippet.thumbnails.default.height  
        },
        "duration": video.contentDetails.duration
    })

with open("output.json", mode="w") as f:
    f.write(json.dumps(videos_json))

# Get created playlists
# resp = client.playlists.list(channel_id=channel.id, parts=["snippet", "contentDetails", "id"], max_results=50)
# playlists = []
# while len(playlists) < resp.pageInfo.totalResults:
#     for playlist in resp.items:
#         print((playlist.snippet.title, playlist.id))
#         playlists.append((playlist.snippet.title, playlist.id))
#     page_token = resp.nextPageToken
#     resp = client.playlists.list(channel_id=channel.id, parts=["snippet", "contentDetails"], max_results=50, page_token=page_token)
