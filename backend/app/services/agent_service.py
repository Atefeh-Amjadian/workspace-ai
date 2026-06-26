from sqlalchemy.orm import Session

from app.models.agent_run import AgentRun
from app.services import email_service
from app.services.report_service import build_email_report
from app.services.telegram_service import send_telegram_message


def run_email_agent(db: Session):
    emails = email_service.sync_unread_gmail_emails(db=db)

    report = build_email_report(db=db)
    telegram_sent = send_telegram_message(report)

    agent_run = AgentRun(
        agent_name="email_agent",
        status="completed",
        synced_emails=len(emails),
        processed_emails=0,
        telegram_sent=telegram_sent,
    )

    db.add(agent_run)
    db.commit()

    return {
        "synced_emails": len(emails),
        "processed_emails": 0,
        "telegram_sent": telegram_sent,
    }

def get_recent_agent_runs(db: Session, limit: int = 5):
    return (
        db.query(AgentRun)
        .order_by(AgentRun.id.desc())
        .limit(limit)
        .all()
    )