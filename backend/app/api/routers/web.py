from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.email import Email
from app.services import email_service
from app.services.dashboard_service import get_email_stats
from app.services.email_service import get_emails
from app.services.gmail_service import GmailAuthError

router = APIRouter(tags=["web"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/emails-dashboard")
def emails_dashboard(request: Request, db: Session = Depends(get_db)):
    stats = get_email_stats(db=db)
    emails = get_emails(db=db)

    return templates.TemplateResponse(
        request=request,
        name="emails_dashboard.html",
        context={
            "stats": stats,
            "emails": emails,
        },
    )


@router.post("/web/sync-gmail")
def web_sync_gmail(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        emails = email_service.sync_unread_gmail_emails(db=db)
    except GmailAuthError:
        return RedirectResponse(
            url="/emails-dashboard?error=gmail_auth",
            status_code=303,
        )

    for email in emails:
        background_tasks.add_task(
            email_service.process_email_with_ai,
            email.id,
        )

    return RedirectResponse(url="/emails-dashboard", status_code=303)


@router.post("/web/process-pending")
def web_process_pending(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    emails = email_service.get_pending_or_failed_emails(db=db)

    for email in emails:
        background_tasks.add_task(
            email_service.process_email_with_ai,
            email.id,
        )

    return RedirectResponse(url="/emails-dashboard", status_code=303)


@router.post("/web/retry-failed")
def web_retry_failed(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    emails = (
        db.query(Email)
        .filter(Email.ai_status == "failed")
        .limit(3)
        .all()
    )

    for email in emails:
        background_tasks.add_task(
            email_service.process_email_with_ai,
            email.id,
        )

    return RedirectResponse(url="/emails-dashboard", status_code=303)