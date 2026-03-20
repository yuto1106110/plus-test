import httpx
from services import ytdlp_service

# ──────────────────────────────
# 複数インスタンス設定
# ──────────────────────────────
PLUS_API_URLS = [
    "https://plus-api-teal.vercel.app",
    # 追加したいときはここに足すだけ
    # "https://plus-api-2.vercel.app",
]

INVIDIOUS_URLS = [
    "https://invidious.snopyta.org",
    "https://vid.puffyan.us",
    "https://yt.artemislena.eu",
    "https://invidious.nerdvpn.de",
    # 追加したいときはここに足すだけ
]

# ──────────────────────────────
# 汎用フェッチ（複数URLを順番に試す）
# ──────────────────────────────
async def fetch_first(urls: list, path: str, params: dict = None) -> dict | list:
    for base_url in urls:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{base_url}{path}", params=params)
                if r.status_code == 200:
                    return r.json()
        except Exception:
            continue
    return {}

# ──────────────────────────────
# 動画情報
# ──────────────────────────────
async def get_video(video_id: str, backend: str = "plusapi") -> dict:
    try:
        if backend == "plusapi":
            data = await fetch_first(PLUS_API_URLS, f"/video/{video_id}")
            if data:
                return data

        if backend == "invidious":
            data = await fetch_first(INVIDIOUS_URLS, f"/api/v1/videos/{video_id}")
            if data:
                return _format_invidious_video(data, video_id)

        if backend == "ytdlp":
            return ytdlp_service.get_video_info(video_id)

    except Exception:
        pass

    # 全部失敗したらyt-dlpで直接取得
    try:
        return ytdlp_service.get_video_info(video_id)
    except Exception:
        return {}

# ──────────────────────────────
# 検索
# ──────────────────────────────
async def search(query: str, backend: str = "plusapi", max_results: int = 10) -> list:
    try:
        if backend == "plusapi":
            data = await fetch_first(
                PLUS_API_URLS, "/search/",
                params={"q": query, "max_results": max_results}
            )
            if data:
                return data.get("results", [])

        if backend == "invidious":
            data = await fetch_first(
                INVIDIOUS_URLS, "/api/v1/search",
                params={"q": query, "type": "video"}
            )
            if isinstance(data, list):
                return _format_invidious_search(data, max_results)

    except Exception:
        pass

    return []

# ──────────────────────────────
# チャンネル
# ──────────────────────────────
async def get_channel(channel_id: str, backend: str = "plusapi") -> dict:
    try:
        if backend == "plusapi":
            data = await fetch_first(PLUS_API_URLS, f"/channel/{channel_id}")
            if data:
                return data

        if backend == "invidious":
            data = await fetch_first(INVIDIOUS_URLS, f"/api/v1/channels/{channel_id}")
            if data:
                return _format_invidious_channel(data)

    except Exception:
        pass

    return {}

# ──────────────────────────────
# Invidiousレスポンスの整形
# ──────────────────────────────
def _format_invidious_video(data: dict, video_id: str) -> dict:
    return {
        "id": data.get("videoId"),
        "title": data.get("title"),
        "description": data.get("description"),
        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
        "duration": data.get("lengthSeconds"),
        "view_count": data.get("viewCount"),
        "like_count": data.get("likeCount"),
        "channel": data.get("author"),
        "channel_id": data.get("authorId"),
        "is_live": data.get("liveNow", False),
        "is_short": data.get("lengthSeconds", 999) <= 60,
    }

def _format_invidious_search(data: list, max_results: int) -> list:
    return [
        {
            "id": v.get("videoId"),
            "title": v.get("title"),
            "thumbnail": f"https://i.ytimg.com/vi/{v.get('videoId')}/maxresdefault.jpg",
            "channel": v.get("author"),
            "view_count": v.get("viewCount"),
            "duration": v.get("lengthSeconds"),
        }
        for v in data[:max_results]
    ]

def _format_invidious_channel(data: dict) -> dict:
    return {
        "id": data.get("authorId"),
        "title": data.get("author"),
        "description": data.get("description"),
        "thumbnail": data.get("authorThumbnails", [{}])[-1].get("url"),
        "subscriber_count": data.get("subCount"),
    }
