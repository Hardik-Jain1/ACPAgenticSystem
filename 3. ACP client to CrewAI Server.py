import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart


async def main():
    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(
            agent="policy_agent",
            input=[
                Message(
                    parts=[MessagePart(content=input("Query:"), content_type="text/plain")]
                )
            ],
        )
        print("Answer:", run.output[0].parts[0].content)

if __name__ == "__main__":
    asyncio.run(main())