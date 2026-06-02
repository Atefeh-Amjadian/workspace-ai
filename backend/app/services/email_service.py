from sqlalchemy.orm import Session

from app.models.email import Email
from app.schemas.email import EmailCreate
from app.services.ai_service import generate_text
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

    prompt = f"""
Summarize this email in one concise sentence.

Subject: {email.subject}
Sender: {email.sender}
Category: {email.category}
"""

    summary = generate_text(prompt)

    email.summary = summary

    db.commit()
    db.refresh(email)

    return email

def generate_draft_reply(db: Session, email_id: int) -> Email | None:
    email = get_email_by_id(db=db, email_id=email_id)

    if email is None:
        return None

    prompt = f"""
You are an email assistant.

Write a short, natural, professional reply to the email below.

Rules:
- Maximum 3 sentences.
- Do not include a subject line.
- Do not include placeholders like [Your Name].
- Do not invent details.
- Use clear and simple English.

Email:
Subject: {email.subject}
Sender: {email.sender}
Category: {email.category}
Summary: {email.summary or "No summary available"}
"""

    draft_reply = generate_text(prompt)

    email.draft_reply = draft_reply

    db.commit()
    db.refresh(email)

    return email


def classify_email(db: Session, email_id: int) -> Email | None:
    email = get_email_by_id(db=db, email_id=email_id)

    if email is None:
        return None

    prompt = f"""
You are an email classification assistant.

Classify the email into exactly one of these categories:
urgent
important
fyi
spam

Rules:
- Return only one word.
- Do not explain.
- Do not use punctuation.
- Choose "urgent" only if immediate action is required.
- Choose "important" if it matters but is not urgent.
- Choose "fyi" if it is informational.
- Choose "spam" if it is promotional, irrelevant, or suspicious.

Email:
Subject: {email.subject}
Sender: {email.sender}
Summary: {email.summary or "No summary available"}
"""

    category = generate_text(prompt).lower().strip()

    allowed_categories = {"urgent", "important", "fyi", "spam"}

    if category not in allowed_categories:
        category = "fyi"

    email.category = category

    db.commit()
    db.refresh(email)

    return email


def sync_unread_gmail_emails(db: Session) -> list[Email]:
    gmail_emails = get_unread_emails()

    saved_emails = []

    for gmail_email in gmail_emails:
        email = Email(
            subject=gmail_email["subject"],
            sender=gmail_email["sender"],
            category="fyi",
        )

        db.add(email)
        saved_emails.append(email)

    db.commit()

    for email in saved_emails:
        db.refresh(email)

    return saved_emails