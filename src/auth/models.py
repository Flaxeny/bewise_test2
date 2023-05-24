from sqlalchemy.orm import Mapped, mapped_column
from src.models import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    UUID: Mapped[str] = mapped_column(nullable=False, unique=True)
