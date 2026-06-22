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
from app.services.report_service import build_email_report
from app.services.telegram_service import send_telegram_message

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


@router.get("/emails-dashboard/{email_id}")
def email_detail(
    email_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    email = email_service.get_email_by_id(db=db, email_id=email_id)

    if email is None:
        return RedirectResponse(
            url="/emails-dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="email_detail.html",
        context={
            "email": email,
        },
    )


@router.post("/emails-dashboard/{email_id}/generate-reply")
def web_generate_reply(
    email_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    email = email_service.get_email_by_id(db=db, email_id=email_id)

    if email is None:
        return RedirectResponse(url="/emails-dashboard", status_code=303)

    if email.ai_status == "processing":
        return RedirectResponse(
            url=f"/emails-dashboard/{email_id}",
            status_code=303,
        )

    email.ai_status = "processing"
    db.commit()

    background_tasks.add_task(
        email_service.process_email_with_ai,
        email_id,
    )

    return RedirectResponse(
        url=f"/emails-dashboard/{email_id}",
        status_code=303,
    )

@router.post("/web/send-telegram-report")
def web_send_telegram_report(
    db: Session = Depends(get_db),
):
    report = build_email_report(db=db)
    send_telegram_message(report)

    return RedirectResponse(
        url="/emails-dashboard",
        status_code=303,
    )