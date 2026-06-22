from sqlalchemy.orm import Session

from app.models.email import Email
from app.services.dashboard_service import get_email_stats


def build_email_report(db: Session) -> str:
    stats = get_email_stats(db=db)

    latest_emails = (
        db.query(Email)
        .order_by(Email.id.desc())
        .limit(5)
        .all()
    )

    report_lines = [
        "📬 Workspace AI Email Report",
        "",
        f"Total Emails: {stats['total_emails']}",
        f"🚨 Urgent: {stats['urgent']}",
        f"⭐ Important: {stats['important']}",
        f"📌 FYI: {stats['fyi']}",
        f"🗑 Spam: {stats['spam']}",
        "",
        "Latest Emails:",
    ]

    for email in latest_emails:
        report_lines.append(
            f"- [{email.category}] {email.subject}"
        )

    return "\n".join(report_lines)