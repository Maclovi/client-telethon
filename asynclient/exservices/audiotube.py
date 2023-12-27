from typing import Any
from urllib.request import urlretrieve

import pytube

from utils import utils

from ..client import AudioProperty, client
from ..lexicon import LEXICON_RU
from ..settings import secrets
from . import request


class CustomTube(pytube.YouTube):
    BASE_DIR: str = "static/"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs |= {"use_oauth": True, "allow_oauth_cache": True}
        super().__init__(*args, **kwargs)
        self.bypass_age_gate()
        self._retical: str = ""
        self._min: int = 0
        self._audio: pytube.Stream | None = None

    @property
    def audio(self) -> pytube.Stream:
        if self._audio:
            return self._audio
        audio: pytube.Stream | None = self.streams.get_audio_only()
        if not isinstance(audio, pytube.Stream):
            raise TypeError(f"error from valid_audio, "
                            f"object audio is not Stream.\n"
                            f"your object={self.audio.__class__}")
        if (gb := audio.filesize_gb) >= 1.5:
            raise TypeError(f"error from valid_audio, limit - 1.5gb\n"
                            f"your filesize - {gb}gb.")
        self._audio = audio
        return self._audio

    @audio.setter
    def audio(self, value: pytube.Stream) -> None:
        self._audio = value

    @property
    def retical(self) -> str:
        if self._retical:
            return self._retical
        if (date := self.publish_date) is None:
            raise TypeError(
                "error from AudioTube(init) with youtube.publish_date\n"
                "your youtube.publish_date={0}, it should be date"
            )
        self._retical = (
            LEXICON_RU["caption"].format(views=self.views, year=date.year)
        )
        return self._retical

    @retical.setter
    def retical(self, value) -> None:
        self._retical = value

    @property
    def min(self) -> int:
        if self._min:
            return self._min
        gb: float = self.audio.filesize_gb
        if gb >= 1.5:
            raise TypeError("filesize too large")
        count_mb: float = .045
        self._min += int(gb / count_mb) + bool(gb % count_mb)
        return self._min

    @min.setter
    def min(self, value):
        self._min = value

    @property
    def audio_property(self) -> AudioProperty:
        return AudioProperty(
            file_path=f"{self.BASE_DIR}{self.title}.mp3",
            thumb_path=f"{self.BASE_DIR}{self.title}.jpeg",
            video_id=self.video_id,
            duration=self.length,
            title=self.title,
            author=self.author,
        )

    def _download_all(self, path) -> None:
        """download audio and thumb"""
        self.audio.download(path, f"{self.title}.mp3")
        urlretrieve(self.thumbnail_url, f"{path}{self.title}.jpeg")

    async def send_audio(self) -> str:
        return await client.send_audio(
            entity=secrets.MUSIC_BACKUP_ID,
            properties=AudioProperty(
                file_path=f"{self.BASE_DIR}{self.title}.mp3",
                thumb_path=f"{self.BASE_DIR}{self.title}.jpeg",
                video_id=self.video_id,
                duration=self.length,
                title=self.title,
                author=self.author,
            )
        )

    async def send_file(self, data: dict[str, Any]) -> None:
        self._download_all(self.BASE_DIR)
        file_id: str = await self.send_audio()
        data |= {
            "file_id": file_id,
            "caption": self.retical,
            "video_id": self.video_id,
        }
        response: str = await request.ping_send(data)
        utils.clear_dir(self.BASE_DIR)
        if response == "ok":
            return print("done")

        raise TypeError("Отправка файла из функции send_file не удалась")
