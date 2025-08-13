import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart
from colorama import Fore

async def main():
    async with Client(base_url="http://localhost:8000") as hospital, Client(base_url="http://localhost:8001") as insurer:
        run1 = await hospital.run_sync(
            agent="health_agent",
            input=[
                Message(
                    parts=[MessagePart(content="Do I need rehabilitation after a shoulder reconstruction?", content_type="text/plain")]
                )
            ],
        )
        content1 = run1.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX + "Hospital Agent Answer:\n", content1 + Fore.RESET)

        run2 = await insurer.run_sync(
            agent="policy_agent",
            input=[
                Message(
                    parts=[MessagePart(content=f"Context: {content1} What is the waiting period for rehabilitation?", content_type="text/plain")]
                )
            ],
        )
        content2 = run2.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX + "Policy Agent Answer:\n", content2 + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(main())