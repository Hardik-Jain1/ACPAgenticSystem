from smolagents import LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool, ToolCallingAgent, ToolCollection
from mcp import StdioServerParameters

model = LiteLLMModel(
    model_id="ollama/qwen2.5:7b",
    api_base="http://localhost:11434",
    # api_key="your-api-key",
    num_ctx=8192,
)

server_parameters = StdioServerParameters(
    command="uv",
    args=["run", "mcp_server.py"],
    env=None
)

def agent(query: str) -> str:
    """This is a Agent which supports the hospital to handle general health based questions for patients. Current or prospective patients can use it to find answers about any general health and hospital treatments.
    """

    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        agent = ToolCallingAgent(
            model=model,
            tools=[*tool_collection.tools, DuckDuckGoSearchTool(), VisitWebpageTool()]
        )

        output = agent.run(query)

    return str(output)
    