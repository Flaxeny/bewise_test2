from fastapi import HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        raise HTTPException(
            status_code=503,
            detail=f'Server closed the connection unexpectedly: {e}'
        )
    finally:
        db.close()
