import httpx

BASE_URL = "https://plus-api-teal.vercel.app"

async def get_video(video_id: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{BASE_URL}/video/{video_id}")
        return r.json()

async def search(query: str, max_results: int = 10) -> list:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{BASE_URL}/search/", params={"q": query, "max_results": max_results})
        return r.json().get("results", [])

async def get_channel(channel_id: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{BASE_URL}/channel/{channel_id}")
        return r.json()
