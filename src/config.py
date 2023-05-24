import os
from uuid import UUID

from dotenv import load_dotenv

from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """The settings class that the pydantic uses to work with environment variables."""

    class Config:
        env_file = '../.env'

    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_USER: str = os.environ.get("DB_USER")
    POSTGRES_PASSWORD: str = os.environ.get("DB_PASS")
    POSTGRES_HOST: str = os.environ.get("DB_HOST")
    POSTGRES_PORT: str = os.environ.get("DB_PORT")
    POSTGRES_DRIVERNAME : str = os.environ.get("DB_DRIVERNAME")


settings = Settings()

DATABASE_URL = f'{settings.POSTGRES_DRIVERNAME}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}' \
               f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'

audio_url = os.environ.get("AUDIO_URL", f"http://localhost:{config.port}")

prefix_task2 = os.environ.get("PREFIX_TASK2", "/task2")

record_path = os.environ.get("RECORD_PATH", "/record")


def get_audio_url(user_id: UUID, audio_id: UUID) -> str:
    return (
        f"{audio_url}{prefix_task2}{record_path}?user_id={user_id}&audio_id={audio_id}"
    )


add_audio_path = os.environ.get("ADD_AUDIO_PATH", "/add_audio")

add_user_path = os.environ.get("ADD_USER_PATH", "/add_user")
