from sqlalchemy.orm import Session

from app.models.email import Email
from app.services.dashboard_service import get_email_stats


def build_email_report(db: Session) -> str:
    stats = get_email_stats(db=db)

    urgent_emails = (
        db.query(Email)
        .filter(Email.category == "urgent")
        .order_by(Email.id.desc())
        .limit(3)
        .all()
    )

    important_emails = (
        db.query(Email)
        .filter(Email.category == "important")
        .order_by(Email.id.desc())
        .limit(3)
        .all()
    )

    report_lines = [
        "📬 Workspace AI Smart Brief",
        "",
        f"You have {stats['urgent']} urgent emails and {stats['important']} important emails.",
        "",
        "Top priorities:",
    ]

    for email in urgent_emails:
        report_lines.append(f"🚨 {email.subject}")

    for email in important_emails:
        report_lines.append(f"⭐ {email.subject}")

    report_lines.extend(
        [
            "",
            f"Processed emails: {stats['total_emails']}",
            "",
            "Recommended action:",
            "Review urgent security and job-related emails first.",
        ]
    )

    return "\n".join(report_lines)