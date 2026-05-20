# email-finder-mcp

A small [MCP](https://modelcontextprotocol.io) server that finds the professional email address of a person given their full name and a company domain. Built with [FastMCP](https://github.com/jlowin/fastmcp), backed by the [AnyMailFinder](https://anymailfinder.com) API.

Originally built to support NGO outreach workflows — looking up contacts at partner organizations from inside an LLM client.

## Tools

- `find_email(full_name, company_domain)` — returns AnyMailFinder's best guess for the person's professional email.

## Requirements

- Python 3.11+
- An [AnyMailFinder](https://anymailfinder.com) API key
- [`uv`](https://docs.astral.sh/uv/) — [install here](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

```bash
git clone https://github.com/SreejeethRamprasad/email-finder-mcp.git
cd email-finder-mcp
uv sync
```

## Use it from Claude Desktop

1. Open your Claude Desktop MCP config file:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the following, replacing the two placeholder values:

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

- Replace `/absolute/path/to/email-finder-mcp` with the full path to the cloned folder (e.g. `/Users/yourname/email-finder-mcp` on macOS).
- Replace `your_key_here` with your AnyMailFinder API key.

3. Save the file and restart Claude Desktop. The `find_email` tool will appear in the tool picker.

## License

MIT — see [LICENSE](LICENSE).
