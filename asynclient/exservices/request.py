from typing import Any

import aiohttp

from ..settings.config import secrets

BASE_URL = secrets.HOST_ASYNCBOT


async def ping_send(data: dict[str, Any]) -> str:
    conf_session = aiohttp.ClientSession(
        base_url=BASE_URL,
        connector=aiohttp.TCPConnector(ssl=False),
        timeout=aiohttp.ClientTimeout(total=15),
    )
    try:
        async with conf_session as session:
            async with session.post('/pong_send', json=data) as response:
                if response.status == 202:
                    return "ok"
    except (TimeoutError, Exception) as e:
        print("Error ->>> ", e)

    return ""
