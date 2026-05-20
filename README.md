# email-finder-mcp

A small [MCP](https://modelcontextprotocol.io) server that finds the professional email address of a person given their full name and a company domain. Built with [FastMCP](https://github.com/jlowin/fastmcp), backed by the [AnyMailFinder](https://anymailfinder.com) API.

Originally built to support NGO outreach workflows — looking up contacts at partner organizations from inside an LLM client.

## Tools

- `find_email(full_name, company_domain)` — returns AnyMailFinder's best guess for the person's professional email.

## Requirements

- Python 3.11+
- An [AnyMailFinder](https://anymailfinder.com) API key
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

## Setup

```bash
git clone https://github.com/SreejeethRamprasad/email-finder-mcp.git
cd email-finder-mcp
uv sync
```

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
# then edit .env
```

The server auto-loads `.env` on startup — no `export` needed.

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
