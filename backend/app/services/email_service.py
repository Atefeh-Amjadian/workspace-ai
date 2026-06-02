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
You are an email assistant.

Summarize this email in one concise sentence.

Email:
Subject: {email.subject}
Sender: {email.sender}
Snippet: {email.snippet or "No email content available"}
Category: {email.category}

Rules:
- Keep it short.
- Do not invent details.
- Use clear and simple English.
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

Email:
Subject: {email.subject}
Sender: {email.sender}
Snippet: {email.snippet or "No email content available"}
Category: {email.category}
Summary: {email.summary or "No summary available"}

Rules:
- Maximum 3 sentences.
- Do not include a subject line.
- Do not include placeholders like [Your Name].
- Do not invent details.
- Use clear and simple English.
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

Email:
Subject: {email.subject}
Sender: {email.sender}
Snippet: {email.snippet or "No email content available"}
Summary: {email.summary or "No summary available"}

Rules:
- Return only one word.
- Do not explain.
- Do not use punctuation.
- Choose "urgent" only if immediate action is required.
- Choose "important" if it matters but is not urgent.
- Choose "fyi" if it is informational.
- Choose "spam" if it is promotional, irrelevant, or suspicious.
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
        saved_emails.append(email)

    db.commit()

    for email in saved_emails:
        db.refresh(email)

    return saved_emails