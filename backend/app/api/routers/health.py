import logging

from fastapi import APIRouter,Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.dependencies import get_db


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/health")
def health_check():
    logger.info("Health endpoint called")
    return {"status": "ok"}

@router.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "database": result.scalar(),
    }