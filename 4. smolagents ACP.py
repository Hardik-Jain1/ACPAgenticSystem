from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, RunYield, RunYieldResume, Server
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool, ToolCallingAgent, ToolCollection
import logging

model = LiteLLMModel(
    model_id="ollama/qwen2.5:7b",
    api_base="http://localhost:11434",
    # api_key="your-api-key",
    num_ctx=8192,
)

server = Server()

@server.agent()
async def health_agent(input: list[Message],
                       context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is a CodeAgent which supports the hospital to handle general health based questions for patients. Current or prospective patients can use it to find answers about any general health and hospital treatments."""
    #
    #agent defination
    agent = CodeAgent(model=model,
                      tools=[DuckDuckGoSearchTool(), VisitWebpageTool()]
    )
    prompt = input[0].parts[0].content
    task_output= agent.run(prompt)
    #
    yield Message(parts=[MessagePart(content=str(task_output))])

if __name__ == "__main__":
    server.run(port=8000)