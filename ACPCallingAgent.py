from smolagents import Tool, ToolCallingAgent
import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart
from smolagents import LiteLLMModel
import asyncio
import nest_asyncio
nest_asyncio.apply()

model = LiteLLMModel(
        model_id="ollama/qwen2.5:7b",
        num_ctx=8192
)

# Tool that wraps an ACP agent server using acp_sdk
class ACPAgentTool(Tool):
    def __init__(self, name, description, client):
        super().__init__()
        self.name = name
        self.description = description
        self.inputs = {"input": {"type": "string", "description": "Input string for the ACP agent"}}
        self.output_type = "string"

        # Create ACP client for this server
        self.client = client

    def forward(self, input: str) -> str:
        try:
            async def _call_agent():
                return await self.client.run_sync(
                    agent=self.name,
                    input=[
                        Message(
                            parts=[MessagePart(content=input, content_type="text/plain")]
                        )
                    ],
                )

            # Run the async code inside this sync function
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(_call_agent())
            
            return result.output[0].parts[0].content
        except Exception as e:
            return f"Error calling ACP agent: {e}"

async def acp_agent_as_tools():
    insurer= Client(base_url="http://localhost:8001")
    hospital= Client(base_url="http://localhost:8000")
    clients = [insurer, hospital]

    collection_agents = []
    for client in clients:
        async for agent in client.agents():
            collection_agents.append((client,agent))

    acp_agents = {agent.name: {'agent': agent, 
                               'description': agent.description, 'client': client
                               } for client, agent in collection_agents}

    # Create ACPAgentTool instances for each agent in acp_agents
    tools = []
    for name, info in acp_agents.items():
        tool = ACPAgentTool(
            name=name,
            description=info['description'],
            client=info['client']
        )
        tools.append(tool)

    return tools

async def router_agent() -> None:
    agent_tools = await acp_agent_as_tools()

    # Create router agent that can call either ACP agent
    router_agent = ToolCallingAgent(
        model=model,
        tools=agent_tools,
        max_steps=5
    )
    return router_agent

async def run_router_agent() -> None:
    router_agent = await router_agent()
    
    final_output = router_agent.run("What are the recommended hospital treatments and recovery guidelines for shoulder reconstruction injury and what is the waiting period for rehabilitation after a shoulder reconstruction from my insurance?")

    print("Final Output: \n", final_output)

if __name__ == "__main__":
    asyncio.run(run_router_agent())
