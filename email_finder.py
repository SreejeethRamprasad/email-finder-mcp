import os
import httpx
from fastmcp import FastMCP

mcp = FastMCP("Email Finder")

API_KEY = os.environ.get("ANYMAILFINDER_API_KEY", "")

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

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)