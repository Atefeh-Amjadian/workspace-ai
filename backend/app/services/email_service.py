from sqlalchemy.orm import Session

from app.models.email import Email
from app.schemas.email import EmailCreate
from app.services.ai_service import classify_text, generate_reply, summarize_text
from app.services.gmail_service import get_unread_emails

def create_email(db: Session, email_data: EmailCreate) -> Email:
    email = Email(
        subject=email_data.subject,
        sender=email_data.sender,
        gmail_id=email_data.gmail_id,
        snippet=email_data.snippet,
        category=email_data.category,
    )

    db.add(email)
    db.commit()
    db.refresh(email)

    return email


def get_emails(db: Session) -> list[Email]:
    return db.query(Email).order_by(Email.id.desc()).all()


def get_email_by_id(db: Session, email_id: int) -> Email | None:
    return db.query(Email).filter(Email.id == email_id).first()


def summarize_email(db: Session, email_id: int) -> Email | None:
    email = get_email_by_id(db=db, email_id=email_id)

    if email is None:
        return None

    summary = summarize_text(
    subject=email.subject,
    sender=email.sender,
    snippet=email.snippet,
    category=email.category,
    )

    email.summary = summary

    db.commit()
    db.refresh(email)

    return email

def generate_draft_reply(db: Session, email_id: int) -> Email | None:
    email = get_email_by_id(db=db, email_id=email_id)

    if email is None:
        return None

    draft_reply = generate_reply(
    subject=email.subject,
    sender=email.sender,
    snippet=email.snippet,
    category=email.category,
    summary=email.summary,
    )

    email.draft_reply = draft_reply

    db.commit()
    db.refresh(email)

    return email


def classify_email(db: Session, email_id: int) -> Email | None:
    email = get_email_by_id(db=db, email_id=email_id)

    if email is None:
        return None

    category = classify_text(
    subject=email.subject,
    sender=email.sender,
    snippet=email.snippet,
    summary=email.summary,
    )

    email.category = category

    db.commit()
    db.refresh(email)

    return email


def sync_unread_gmail_emails(db: Session) -> list[Email]:
    gmail_emails = get_unread_emails()

    saved_emails = []

    for gmail_email in gmail_emails:
        existing_email = (
            db.query(Email)
            .filter(Email.gmail_id == gmail_email["gmail_id"])
            .first()
        )

        if existing_email:
            continue

        email = Email(
            subject=gmail_email["subject"],
            sender=gmail_email["sender"],
            gmail_id=gmail_email["gmail_id"],
            snippet=gmail_email["snippet"],
            category="fyi",
        )

        db.add(email)
        db.flush()

        email.summary = summarize_text(
            subject=email.subject,
            sender=email.sender,
            snippet=email.snippet,
            category=email.category,
        )

        email.category = classify_text(
            subject=email.subject,
            sender=email.sender,
            snippet=email.snippet,
            summary=email.summary,
        )

        email.draft_reply = generate_reply(
            subject=email.subject,
            sender=email.sender,
            snippet=email.snippet,
            category=email.category,
            summary=email.summary,
        )

        saved_emails.append(email)

    db.commit()

    for email in saved_emails:
        db.refresh(email)

    return saved_emails