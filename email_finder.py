import base64
import os
import stat
from email.mime.text import MIMEText
from pathlib import Path
from threading import Lock

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv(Path(__file__).parent / ".env")

mcp = FastMCP("NGO Outreach")

API_KEY = os.environ.get("ANYMAILFINDER_API_KEY", "")

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
TOKEN_PATH = Path(__file__).parent / "token.json"

_creds: Credentials | None = None
_creds_lock = Lock()


def _load_gmail_service():
    """Load (and refresh if needed) Gmail credentials, return a Gmail API service.

    Caches credentials in module scope so we don't re-read token.json on every call.
    Refresh happens only when the access token has actually expired.
    """
    global _creds
    with _creds_lock:
        if _creds is None:
            if not TOKEN_PATH.exists():
                raise RuntimeError(
                    f"{TOKEN_PATH.name} not found. Run `python authorize_gmail.py` once to grant access."
                )
            _creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), GMAIL_SCOPES)

        if not _creds.valid:
            if _creds.expired and _creds.refresh_token:
                _creds.refresh(Request())
                TOKEN_PATH.write_text(_creds.to_json())
                os.chmod(TOKEN_PATH, stat.S_IRUSR | stat.S_IWUSR)
            else:
                raise RuntimeError(
                    "Gmail credentials are invalid and cannot be refreshed. "
                    "Re-run `python authorize_gmail.py`."
                )

    return build("gmail", "v1", credentials=_creds, cache_discovery=False)


@mcp.tool()
async def find_email(full_name: str, company_domain: str) -> dict:
    """
    Find the professional email of a person.
    Args:
        full_name: The person's full name e.g. "Himanshu Giri"
        company_domain: The company's domain e.g. "prathambooks.org"
    """
    if not API_KEY:
        return {"error": "API key not set. Set ANYMAILFINDER_API_KEY env variable."}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anymailfinder.com/v5.0/search/person.json",
            headers={"X-Api-Key": API_KEY},
            json={
                "full_name": full_name,
                "domain": company_domain
            }
        )
        return response.json()


@mcp.tool()
def create_draft(
    to: str,
    subject: str,
    body: str,
    cc: str | None = None,
    bcc: str | None = None,
) -> dict:
    """
    Create a Gmail draft in the authenticated user's account.
    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: HTML email body. Use tags like <b>, <u>, <i>, <a href="...">, and <br> for line breaks. Plain newlines in the body are converted to <br> automatically.
        cc: Optional CC recipient(s), comma-separated.
        bcc: Optional BCC recipient(s), comma-separated.
    Returns:
        {"draft_id", "message_id", "thread_id"} on success, or {"error": ...}.
    """
    try:
        service = _load_gmail_service()
    except RuntimeError as e:
        return {"error": str(e)}

    html_body = body if ("<br" in body.lower() or "<p" in body.lower()) else body.replace("\n", "<br>")
    message = MIMEText(html_body, "html", "utf-8")
    message["To"] = to
    message["Subject"] = subject
    if cc:
        message["Cc"] = cc
    if bcc:
        message["Bcc"] = bcc

    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body={"message": {"raw": encoded}})
            .execute()
        )
    except HttpError as e:
        return {"error": f"Gmail API error: {e}"}

    msg = draft.get("message", {})
    return {
        "draft_id": draft.get("id"),
        "message_id": msg.get("id"),
        "thread_id": msg.get("threadId"),
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
