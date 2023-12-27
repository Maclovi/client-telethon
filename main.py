import asyncio
import logging

from aiohttp import web
from aiojobs.aiohttp import setup

from asynclient.client import client
from asynclient.views import client_bot
from views import base

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING,
    filename="asynclient/settings/logs.log"
)


def main() -> None:
    loop = asyncio.get_event_loop()
    client.start()
    app: web.Application = web.Application()  # client max size 1mb.
    app.add_routes(client_bot.routes)
    app.add_routes(base.routes)
    setup(app)
    web.run_app(app, host="0.0.0.0", port=8080, loop=loop)


if __name__ == "__main__":
    main()
