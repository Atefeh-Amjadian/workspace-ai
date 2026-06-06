from sqlalchemy.orm import Session

from app.models.email import Email
from sqlalchemy import func

def get_email_stats(db: Session) -> dict:
    total_emails = db.query(Email).count()

    urgent = db.query(Email).filter(Email.category == "urgent").count()
    important = db.query(Email).filter(Email.category == "important").count()
    fyi = db.query(Email).filter(Email.category == "fyi").count()
    spam = db.query(Email).filter(Email.category == "spam").count()

    return {
        "total_emails": total_emails,
        "urgent": urgent,
        "important": important,
        "fyi": fyi,
        "spam": spam,
    }


def get_top_senders(db: Session):
    results = (
        db.query(
            Email.sender,
            func.count(Email.id).label("count")
        )
        .group_by(Email.sender)
        .order_by(func.count(Email.id).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "sender": sender,
            "count": count,
        }
        for sender, count in results
    ]