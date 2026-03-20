import yt_dlp

BASE_OPTS = {
    "quiet": True,
    "no_warnings": True,
}

def get_video_info(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(BASE_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "id": info.get("id"),
            "title": info.get("title"),
            "description": info.get("description"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "like_count": info.get("like_count"),
            "channel": info.get("channel"),
            "channel_id": info.get("channel_id"),
            "upload_date": info.get("upload_date"),
            "is_live": info.get("is_live", False),
            "is_short": info.get("duration", 999) <= 60,
        }
