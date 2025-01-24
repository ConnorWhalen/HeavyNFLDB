import json

INPUT_FILENAME = "videos-typed.json"
OUTPUT_FILENAME = "podcasts.json"

with open(INPUT_FILENAME) as input_file:
    videos = json.loads(input_file.read())


filtered_videos = [video for video in videos if video["type"] == "podcast"]

with open(OUTPUT_FILENAME, mode="w") as output_file:
    output_file.write(json.dumps(filtered_videos))
