from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.auth.models import User


def get_user_from_database(username: str, db: Session) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    return user


def _create_user(username: str, db: Session) -> User:
    user = get_user_from_database(username, db)
    if user is not None:
        raise HTTPException(
            status_code=409,
            detail='User with this username already exists'
        )
    user = User(
        username=username,
        UUID=str(uuid4())
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
