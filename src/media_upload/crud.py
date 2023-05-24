import io
from uuid import uuid4

from fastapi import HTTPException
from pydub import AudioSegment
from sqlalchemy.orm import Session

from src.auth.models import User
from src.media_upload.models import Media

from pydub.exceptions import CouldntDecodeError


def get_user_from_database_by_id_and_UUID(id: int,
                                          UUID: str,
                                          db: Session) -> User | None:
    user = db.query(User).filter(User.id == id, User.UUID == UUID).first()
    return user


def convert_wav_in_mp3(audio_file: bytes) -> bytes:
    wav_audio = AudioSegment.from_wav(io.BytesIO(audio_file))
    mp3_audio = io.BytesIO()
    wav_audio.export(mp3_audio, format='mp3')
    mp3_audio.seek(0)
    mp3_data = mp3_audio.read()
    return mp3_data


def _upload_media(id: int, UUID: str,
                  audio_file: bytes, db: Session) -> Media:
    user = get_user_from_database_by_id_and_UUID(id, UUID, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='User do not exists'
        )
    try:
        mp3_file = convert_wav_in_mp3(audio_file)
        media = Media(
            author=user.id,
            UUID=str(uuid4()),
            file=mp3_file
        )
        db.add(media)
        db.commit()
        db.refresh(media)
        return media
    except CouldntDecodeError as e:
        raise HTTPException(
            status_code=422,
            detail=f'Wrong file format: {e}'
        )
