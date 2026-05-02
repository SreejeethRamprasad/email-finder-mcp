# email-finder-mcp

A small [MCP](https://modelcontextprotocol.io) server that finds the professional email address of a person given their full name and a company domain. Built with [FastMCP](https://github.com/jlowin/fastmcp), backed by the [AnyMailFinder](https://anymailfinder.com) API.

Originally built to support NGO outreach workflows — looking up contacts at partner organizations from inside an LLM client.

## Tools

- `find_email(full_name, company_domain)` — returns AnyMailFinder's best guess for the person's professional email.
- `create_draft(to, subject, body, cc?, bcc?)` — creates a draft in your Gmail account.

## Requirements

- Python 3.11+
- An [AnyMailFinder](https://anymailfinder.com) API key
- A Google Cloud OAuth Desktop client (for `create_draft`) — see Gmail setup below
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

## Setup

```bash
git clone https://github.com/SreejeethRamprasad/email-finder-mcp.git
cd email-finder-mcp
uv sync
```

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
# then edit .env
```

The server auto-loads `.env` on startup — no `export` needed.

## One-time Gmail setup (for `create_draft`)

1. In [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials), create an **OAuth client ID** of type **Desktop app**. Note the client ID and secret.
2. On the OAuth consent screen, add the scope `https://www.googleapis.com/auth/gmail.compose` and add your Gmail account as a test user (if the app is in "Testing" mode).
3. Add the credentials to your `.env`:

   ```
   GOOGLE_OAUTH_CLIENT_ID=...
   GOOGLE_OAUTH_CLIENT_SECRET=...
   ```

4. Run the bootstrapper once:

   ```bash
   uv run python authorize_gmail.py
   ```

   A browser window opens — grant access. A `token.json` (chmod 600) is written next to the script. The MCP server reads from it on each call and silently refreshes when needed.

`token.json` and any `client_secret*.json` are gitignored. Re-run `authorize_gmail.py` only if you revoke access or change scopes.

## Use it from Claude Desktop

Add this to your Claude Desktop MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "email-finder": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/email-finder-mcp",
        "run",
        "python",
        "email_finder.py"
      ],
      "env": {
        "ANYMAILFINDER_API_KEY": "your_key_here"
      }
    }
  }
}
```

Restart Claude Desktop. The `find_email` tool will appear in the tool picker.

## Run it standalone (HTTP)

```bash
uv run python email_finder.py
```

The server will listen on `http://127.0.0.1:8000`.

## License

MIT — see [LICENSE](LICENSE).
