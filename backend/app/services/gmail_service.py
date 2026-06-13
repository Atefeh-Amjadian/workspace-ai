import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).resolve().parents[2]
CREDENTIALS_PATH = BASE_DIR / "credentials" / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"
class GmailAuthError(Exception):
    pass

def get_gmail_service():
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_unread_emails(max_results: int = 20):
    service = get_gmail_service()

    result = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=["UNREAD"],
            maxResults=max_results,
        )
        .execute()
    )

    messages = result.get("messages", [])

    emails = []

    for message in messages:
        msg = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["Subject", "From"],
            )
            .execute()
        )

        headers = msg.get("payload", {}).get("headers", [])

        subject = ""
        sender = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]
            elif header["name"] == "From":
                sender = header["value"]

        emails.append(
            {
                "gmail_id": msg["id"],
                "subject": subject,
                "sender": sender,
                "snippet": msg.get("snippet", ""),
            }
        )

    return emails