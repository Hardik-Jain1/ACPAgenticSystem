from smolagents import LiteLLMModel, ToolCallingAgent, ToolCollection
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
    """This ia an agent which uses the tools from a MCP server to answer questions around policy coverage and to handle general health based questions for patients."""

    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        agent = ToolCallingAgent(
            model=model,
            tools=[*tool_collection.tools]
        )
        output = agent.run(query)

    return str(output)

if __name__ == "__main__":
    ans = agent(input("Query: "))
    print("Answer:", ans)