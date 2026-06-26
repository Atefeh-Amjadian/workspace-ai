from sqlalchemy.orm import Session

from app.models.agent_run import AgentRun
from app.services import email_service
from app.services.report_service import build_email_report
from app.services.telegram_service import send_telegram_message


def run_email_agent(db: Session):
    emails = email_service.sync_unread_gmail_emails(db=db)

    for email in emails[:2]:
        email_service.process_email_with_ai(
            email_id=email.id,
        )

    report = build_email_report(db=db)

    telegram_sent = send_telegram_message(report)

    agent_run = AgentRun(
        agent_name="email_agent",
        status="completed",
        synced_emails=len(emails),
        processed_emails=min(len(emails), 2),
        telegram_sent=telegram_sent,
    )

    db.add(agent_run)
    db.commit()

    return {
        "synced_emails": len(emails),
        "processed_emails": min(len(emails), 2),
        "telegram_sent": telegram_sent,
    }