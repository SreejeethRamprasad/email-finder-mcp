# email-finder-mcp

A small [MCP](https://modelcontextprotocol.io) server that finds the professional email address of a person given their full name and a company domain. Built with [FastMCP](https://github.com/jlowin/fastmcp), backed by the [AnyMailFinder](https://anymailfinder.com) API.

Originally built to support NGO outreach workflows — looking up contacts at partner organizations from inside an LLM client.

## Tools

- `find_email(full_name, company_domain)` — returns AnyMailFinder's best guess for the person's professional email.

## Requirements

- An [AnyMailFinder](https://anymailfinder.com) API key
- A [Prefect Horizon](https://horizon.prefect.io) account (free tier works)
- A GitHub account

## Deploy your own instance

Each user deploys their own instance so they use their own AnyMailFinder quota.

Prefect Horizon can only deploy repos in *your own* GitHub account, so the first step is to fork this one.

1. **Fork this repo.** Go to `https://github.com/SreejeethRamprasad/email-finder-mcp` and click **Fork** (top right). This creates a copy under your own GitHub account.
2. Sign in to [Prefect Horizon](https://horizon.prefect.io) and start creating a new MCP server.
3. On the **Select a repository to deploy** screen, choose your fork (`your-username/email-finder-mcp`). If it doesn't appear, click **Check permissions** / **Refresh** and grant the Prefect GitHub App access to the fork.
4. On the deploy screen, set the **Entrypoint** to:
   ```
   email_finder.py:mcp
   ```
   (This points Prefect at the `mcp` server object in `email_finder.py`. Leaving it blank may work via auto-detection, but setting it explicitly is more reliable.)
5. Add your API key as an environment variable (under **Advanced Configuration**, or in the server's settings after deploying):
   ```
   ANYMAILFINDER_API_KEY=your_key_here
   ```
6. Click **Deploy Server**. Prefect will give you a URL like `https://your-server-name.fastmcp.app/mcp`.

No local Python setup or cloning required — just the fork.

## Connect to Claude

Works the same way on both Claude.ai (web) and Claude Desktop:

1. Go to **Settings → Connectors → Add custom connector**
2. Enter a name (e.g. `Email Finder`) and paste your Prefect URL.
3. Click **Add** — the `find_email` tool will appear in your conversations.

## License

MIT — see [LICENSE](LICENSE).
