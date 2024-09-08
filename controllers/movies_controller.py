from flask import Blueprint, render_template
from repositories.youtube_repository import get_my_recent_videos
from services.postback_service import get_or_default, no_icon_image_public_url

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/movies')
def show_movies():
    youtube_videos = get_my_recent_videos()

    videos = []
    for video in youtube_videos:
        thumbnail_image_url = get_or_default(video, lambda x: x.get("snippet").get("thumbnails").get("high").get("url"), no_icon_image_public_url())
        title = get_or_default(video, lambda x: x.get("snippet").get("title")[:40], " ")
        text = get_or_default(video, lambda x: x.get("snippet").get("description")[:60], " ")
        video_id = get_or_default(video, lambda x: x.get('id').get('videoId'), 'error')
        videos.append({ "thumbnail": thumbnail_image_url, "title": title, "description": text, "id": video_id})
    return render_template('movies.html', videos=videos)
