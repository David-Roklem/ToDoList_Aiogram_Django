from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


class Settings(BaseSettings):

    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")
    bot_token: str
    admin_id: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    CELERY_MAIN: str

    BACKEND_SERVER_ADDRESS: str

    TIMEZONE: str

    DB_URL: str = Field('', validation_alias='DB_URL')
    REDIS_URL: str = Field('', validation_alias='REDIS_URL')

    def __init__(self, **data):
        super().__init__(**data)
        self.DB_URL = self.__construct_db_url()
        self.REDIS_URL = self.__construct_redis_url()

    def __construct_db_url(self) -> str:
        return (f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    def __construct_redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings


settings = get_settings()

bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
