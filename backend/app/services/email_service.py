from sqlalchemy.orm import Session

from app.models.email import Email
from app.schemas.email import EmailCreate


def create_email(db: Session, email_data: EmailCreate) -> Email:
    email = Email(
        subject=email_data.subject,
        sender=email_data.sender,
    )

    db.add(email)
    db.commit()
    db.refresh(email)

    return email


def get_emails(db: Session) -> list[Email]:
    return db.query(Email).order_by(Email.id.desc()).all()


def get_email_by_id(db: Session, email_id: int) -> Email | None:
    return db.query(Email).filter(Email.id == email_id).first()