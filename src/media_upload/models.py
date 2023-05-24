from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.models import Base


class Media(Base):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    author: Mapped[int] = mapped_column(ForeignKey('user.id'))
    UUID: Mapped[str] = mapped_column(nullable=False)
    file: Mapped[bytes] = mapped_column(nullable=False)
