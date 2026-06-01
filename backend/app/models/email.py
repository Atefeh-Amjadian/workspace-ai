from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    sender: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="fyi", nullable=False)

    summary: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    draft_reply: Mapped[str | None] = mapped_column(String(5000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )