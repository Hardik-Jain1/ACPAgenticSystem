import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart
from smolagents import LiteLLMModel
from fastacp import AgentCollection, ACPCallingAgent, ActionStep
from colorama import Fore

model = LiteLLMModel(
        model_id="ollama/qwen2.5:7b",
        num_ctx=8192
) 

async def run_hospital_workflow() -> None:
    async with Client(base_url="http://localhost:8001") as insurer, Client(base_url="http://localhost:8000") as hospital:
        agent_collection = await AgentCollection.from_acp(insurer, hospital)

        acp_agents = {agent.name: {'agent': agent, 'client': client} for client, agent in agent_collection.agents}

        acpagent = ACPCallingAgent(
            model=model,
            acp_agents=acp_agents,
        )

        query= "do i need rehabilitation after a shoulder reconstruction and what is the waiting period from my insurance?"
        result = await acpagent.run(query)

        print(Fore.YELLOW + f"Final result: {result}" + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(run_hospital_workflow())