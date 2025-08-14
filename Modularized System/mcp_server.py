from mcp.server.fastmcp import FastMCP
import json
import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

mcp = FastMCP("agents")

@mcp.tool("policy_tool")
async def policy_tool(query: str) -> str:
    """This is a tool for questions around policy coverage, it uses a RAG pattern to find answers based on policy documentation. Use it to help answer questions on coverage and waiting periods.
    Args:
        query (str): The question or query related to policy coverage.
    Returns:
        str: The response to the query.    
    """
    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(
            agent="policy_agent",
            input=[
                Message(
                    parts=[MessagePart(content=query, content_type="text/plain")]
                )
            ],
        )
        return run.output[0].parts[0].content
            
@mcp.tool("health_tool")
async def health_tool(query: str) -> str:
    """This is a tool which supports the hospital to handle general health based questions for patients. Current or prospective patients can use it to find answers about any general health and hospital treatments.
    Args:
        query (str): The question or query related to health or hospital treatments.
    Returns:
        str: The response to the query.
    """

    async with Client(base_url="http://localhost:8002") as client:
        run = await client.run_sync(
            agent="health_agent",
            input=[
                Message(
                    parts=[MessagePart(content=query, content_type="text/plain")]
                )
            ],
        )
        return run.output[0].parts[0].content

if __name__ == "__main__":
    mcp.run(transport="stdio")