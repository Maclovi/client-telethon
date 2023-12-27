from typing import Any

from aiohttp import web
from aiojobs.aiohttp import spawn

from asynclient.exservices import CustomTube

routes = web.RouteTableDef()


@routes.post("/pong_message")
async def handler_audio(request: web.Request) -> web.Response:
    data: dict[str, Any] = await request.json()
    try:
        youtube = CustomTube(data["url"])
        await spawn(request, youtube.send_file(data))
        return web.json_response({"time": str(youtube.min)}, status=202)
    except Exception:
        return web.json_response(status=500)
