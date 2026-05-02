"""One-time Gmail OAuth bootstrapper.

Run this once: `python authorize_gmail.py`
It opens a browser, you grant access, and a `token.json` is written next to this file.
The MCP server then reads (and silently refreshes) that token on each call.
"""
import json
import os
import stat
import sys
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv(Path(__file__).parent / ".env")

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
TOKEN_PATH = Path(__file__).parent / "token.json"


def main() -> int:
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    if not client_id or not client_secret:
        print(
            "ERROR: GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET must be set.\n"
            "Put them in .env and `source` it, or export them in your shell.",
            file=sys.stderr,
        )
        return 1

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")

    TOKEN_PATH.write_text(creds.to_json())
    os.chmod(TOKEN_PATH, stat.S_IRUSR | stat.S_IWUSR)

    data = json.loads(TOKEN_PATH.read_text())
    print(f"✓ Token saved to {TOKEN_PATH} (chmod 600)")
    print(f"  Scopes: {data.get('scopes')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
