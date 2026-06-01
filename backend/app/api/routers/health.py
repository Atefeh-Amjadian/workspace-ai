import logging

from fastapi import APIRouter

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/health")
def health_check():
    logger.info("Health endpoint called")
    return {"status": "ok"}