# email-finder-mcp

A small [MCP](https://modelcontextprotocol.io) server that finds the professional email address of a person given their full name and a company domain. Built with [FastMCP](https://github.com/jlowin/fastmcp), backed by the [AnyMailFinder](https://anymailfinder.com) API.

Originally built to support NGO outreach workflows — looking up contacts at partner organizations from inside an LLM client.

## Tools

- `find_email(full_name, company_domain)` — returns AnyMailFinder's best guess for the person's professional email.

## Requirements

- An [AnyMailFinder](https://anymailfinder.com) API key
- A [Prefect](https://app.prefect.cloud) account (free tier works)

## Deploy your own instance

Each user deploys their own instance so they use their own AnyMailFinder quota.

1. Sign in to [Prefect Horizon](https://app.prefect.cloud) and create a new MCP server.
2. Connect it to this GitHub repo: `https://github.com/SreejeethRamprasad/email-finder-mcp`
3. In Prefect's environment settings, add:
   ```
   ANYMAILFINDER_API_KEY=your_key_here
   ```
4. Deploy. Prefect will give you a URL like `https://your-server-name.fastmcp.app/mcp`.

No local Python setup or cloning required.

## Connect to Claude

### Claude.ai (web)

1. Go to **Settings → Connectors → Add custom connector**
2. Enter a name (e.g. `Email Finder`) and paste your Prefect URL.
3. Click **Add** — the `find_email` tool will appear in your conversations.

### Claude Desktop

1. Open your MCP config file:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the following, replacing the URL with your own:

```json
{
  "mcpServers": {
    "email-finder": {
      "url": "https://your-server-name.fastmcp.app/mcp"
    }
  }
}
```

3. Save and restart Claude Desktop.

## License

MIT — see [LICENSE](LICENSE).
