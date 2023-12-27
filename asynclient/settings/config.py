from dotenv import dotenv_values


class BaseSettings:
    def __init__(self, *, env: str | None = None) -> None:
        self._converts_of_env(env)

    def _converts_of_env(self, env):
        for k, v in dotenv_values(env).items():
            if k in self.__annotations__:
                setattr(self, k, self.__annotations__[k](v))


class Settings(BaseSettings):
    API_ID: int
    API_HASH: str
    SECRET_PATH: str
    MUSIC_BACKUP_ID: int
    HOST_ASYNCBOT: str


secrets = Settings(env='.env')
