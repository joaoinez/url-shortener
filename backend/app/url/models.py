from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.main import Base


class URL(Base):
    __tablename__: str = "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)
    token: Mapped[str] = mapped_column(String(43))
