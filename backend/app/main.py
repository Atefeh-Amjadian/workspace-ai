from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Workspace Assistant backend",
)

app.include_router(health_router)