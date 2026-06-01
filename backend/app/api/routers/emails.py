from fastapi import APIRouter, Depends,HTTPException
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


@router.get("/", response_model=list[EmailResponse])
def get_emails(db: Session = Depends(get_db)):
    emails = db.query(Email).order_by(Email.id.desc()).all()
    return emails


@router.get("/{email_id}", response_model=EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()

    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email