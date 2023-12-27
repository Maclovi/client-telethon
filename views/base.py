from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/')
async def index(_: web.Request) -> web.Response:
    return web.Response(text='welcome, brauh poapapapap.')
