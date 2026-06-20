from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routers.emails import router as emails_router
from app.api.routers.dashboard import router as dashboard_router
from app.api.routers.web import router as web_router

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Workspace Assistant backend",
)

app.include_router(health_router)
app.include_router(emails_router)
app.include_router(dashboard_router)
app.include_router(web_router)