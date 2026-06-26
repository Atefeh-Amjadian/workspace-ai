from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)

    agent_name = Column(String, nullable=False, default="email_agent")
    status = Column(String, nullable=False, default="completed")

    synced_emails = Column(Integer, nullable=False, default=0)
    processed_emails = Column(Integer, nullable=False, default=0)

    important_emails_found = Column(Boolean, nullable=False, default=False)
    telegram_sent = Column(Boolean, nullable=False, default=False)

    error_message = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )