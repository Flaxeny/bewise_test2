import io
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from src.config import Settings
from src.media_upload.crud import _upload_media
from src.media_upload.models import Media
from src.media_upload.schemas import Url
from src.db import get_db

media_upload_router = APIRouter()


@media_upload_router.post('/',
                          summary='Загрузка аудиофайла',
                          response_model=Url)
def upload_media(id: int,
                 UUID: str,
                 audio_file: Annotated[bytes, File(...)],
                 db: Annotated[Session, Depends(get_db)]) -> Url:
    """Загрузка WAV файла по id и UUID пользователя."""
    upload = _upload_media(id, UUID, audio_file, db)
    url = f'http://{Settings.HOST}:{Settings.PORT}/record?id={upload.id}&user={upload.author}'
    return Url(
        url=url
    )


@media_upload_router.get('/record',
                         summary='Скачивание аудиофайла')
def download_media(id: int, user: int,
                   db: Annotated[Session, Depends(get_db)]):
    """Скачивание MP3 файл по id юзера и id файла."""
    mp3_data = db.query(Media).filter(
        Media.author == user, Media.id == id
        ).first()
    if mp3_data is None:
        raise HTTPException(
            status_code=404,
            detail='File not found'
        )
    content = io.BytesIO(mp3_data.file).read()
    return Response(
        content=content,
        media_type='audio/mpeg',
        headers={
            'Content-Disposition': f'attachment; filename="{mp3_data.id}"'
        }
    )
