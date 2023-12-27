from dataclasses import dataclass

from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
from telethon.types import Message
from telethon.utils import pack_bot_file_id

from .settings import secrets


@dataclass
class AudioProperty:
    file_path: str
    video_id: str
    thumb_path: str
    duration: int
    title: str
    author: str


class UserTelethon(TelegramClient):
    async def send_audio(self, entity: int, properties: AudioProperty) -> str:
        message: Message = await self.send_file(
                entity=entity,
                file=properties.file_path,
                caption=properties.video_id,
                thumb=properties.thumb_path,
                allow_cache=False,
                attributes=[DocumentAttributeAudio(
                    duration=properties.duration,
                    title=properties.title,
                    performer=properties.author,
                )]
        )
        return self.get_file_id(message)

    async def show_all_files(self, entity: int) -> None:
        number: int = 0
        async for message in self.iter_messages(entity):
            if file := message.file:
                number += 1
                print(
                    f"(\n"
                    f"\tnumber: {number}\n"
                    f"\tid: {file.id}\n"
                    f"\ttext: {message.text}\n"
                    f"\ttitle: {file.title}"
                    f"\n)"
                )

    async def sync_db_audio(self, enitity: int) -> None:
        '''Here needs connect to data base'''
        pass

    @classmethod
    def get_file_id(cls, message: Message) -> str:
        file_id: str | None = pack_bot_file_id(message.media)
        if file_id is None:
            raise TypeError("func: get_file_id, wrong: file id is None")
        return file_id


client: UserTelethon = UserTelethon(
        session="me",
        api_id=secrets.API_ID,
        api_hash=secrets.API_HASH,
        device_model="iPhone 11 Pro",
        system_version="IOS 100.1",
    )
