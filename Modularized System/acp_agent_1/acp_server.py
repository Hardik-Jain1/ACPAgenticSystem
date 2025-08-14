from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Server, Context, RunYield, RunYieldResume
from crews.rag_crew import RAGCrew

server = Server()

@server.agent()
async def policy_agent(input: list[Message],
                       context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is an agent for questions around policy coverage, it uses a RAG pattern to find answers based on policy documentation. Use it to help answer questions on coverage and waiting periods."""
    #
    #agent defination
    crew = RAGCrew()
    input_text = input[0].parts[0].content if input else "What is the waiting period for rehabilitation?"
    crew.insurance_task.description = input_text
    task_output = await crew.run_async()
    #
    yield Message(parts=[MessagePart(content=str(task_output))])

if __name__ == "__main__":
    server.run(port=8001)