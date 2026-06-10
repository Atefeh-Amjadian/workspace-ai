from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.email import EmailCreate, EmailResponse
from app.services import email_service

router = APIRouter(prefix="/emails", tags=["emails"])


@router.post("/", response_model=EmailResponse)
def create_email(email_data: EmailCreate, db: Session = Depends(get_db)):
    return email_service.create_email(db=db, email_data=email_data)


@router.get("/", response_model=list[EmailResponse])
def get_emails(db: Session = Depends(get_db)):
    return email_service.get_emails(db=db)


@router.get("/{email_id}", response_model=EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    email = email_service.get_email_by_id(db=db, email_id=email_id)

    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email

@router.post("/{email_id}/summarize", response_model=EmailResponse)
def summarize_email(email_id: int, db: Session = Depends(get_db)):
    try:
        email = email_service.summarize_email(db=db, email_id=email_id)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))

    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email

@router.post("/{email_id}/draft-reply", response_model=EmailResponse)
def generate_draft_reply(email_id: int, db: Session = Depends(get_db)):
    try:
        email = email_service.generate_draft_reply(db=db, email_id=email_id)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))

    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email

@router.post("/{email_id}/classify", response_model=EmailResponse)
def classify_email(email_id: int, db: Session = Depends(get_db)):
    try:
        email = email_service.classify_email(db=db, email_id=email_id)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))

    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email

@router.post("/sync-gmail", response_model=list[EmailResponse])
def sync_gmail_emails(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    emails = email_service.sync_unread_gmail_emails(db=db)

    for email in emails:
        background_tasks.add_task(
            email_service.process_email_with_ai,
            email.id,
        )

    return emails

@router.post("/process-pending")
def process_pending_emails(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    emails = email_service.get_pending_or_failed_emails(db=db)

    for email in emails:
        background_tasks.add_task(
            email_service.process_email_with_ai,
            email.id,
        )

    return {
        "message": "Pending emails processing started",
        "count": len(emails),
    }