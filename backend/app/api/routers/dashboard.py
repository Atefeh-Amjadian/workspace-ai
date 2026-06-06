from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.dashboard_service import get_email_stats, get_top_senders

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    return get_email_stats(db=db)


@router.get("/top-senders")
def dashboard_top_senders(db: Session = Depends(get_db)):
    return get_top_senders(db=db)