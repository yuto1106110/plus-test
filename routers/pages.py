from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from services.backend_manager import get_video, search, get_channel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/index")
async def index(request: Request, q: str = None, backend: str = "plusapi"):
    results = []
    if q:
        results = await search(q, backend=backend)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": results,
        "query": q,
        "backend": backend,
    })

@router.get("/watch")
async def watch(request: Request, v: str = Query(...), backend: str = "plusapi"):
    video = await get_video(v, backend=backend)
    return templates.TemplateResponse("watch.html", {
        "request": request,
        "video": video,
        "backend": backend,
    })

@router.get("/channel/{channel_id}")
async def channel(request: Request, channel_id: str, backend: str = "plusapi"):
    data = await get_channel(channel_id, backend=backend)
    return templates.TemplateResponse("channel.html", {
        "request": request,
        "channel": data,
        "backend": backend,
    })

@router.get("/shorts/{video_id}")
async def shorts(request: Request, video_id: str, backend: str = "plusapi"):
    video = await get_video(video_id, backend=backend)
    return templates.TemplateResponse("shorts.html", {
        "request": request,
        "video": video,
        "backend": backend,
    })

@router.get("/music")
async def music(request: Request, v: str = Query(...), backend: str = "plusapi"):
    video = await get_video(v, backend=backend)
    return templates.TemplateResponse("music.html", {
        "request": request,
        "video": video,
        "backend": backend,
    })
