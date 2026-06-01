from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.email import Email
from app.schemas.email import EmailCreate, EmailResponse

router = APIRouter(prefix="/emails", tags=["emails"])


@router.post("/", response_model=EmailResponse)
def create_email(email_data: EmailCreate, db: Session = Depends(get_db)):
    email = Email(
        subject=email_data.subject,
        sender=email_data.sender,
    )

    db.add(email)
    db.commit()
    db.refresh(email)

    return email
