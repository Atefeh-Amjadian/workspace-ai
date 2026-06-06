from sqlalchemy.orm import Session

from app.models.email import Email


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