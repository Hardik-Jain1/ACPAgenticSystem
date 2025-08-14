from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, RunYield, RunYieldResume, Server
from health_agent import agent

server = Server()

@server.agent()
async def health_agent(input: list[Message],
                       context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is a Agent which supports the hospital to handle general health based questions for patients. Current or prospective patients can use it to find answers about any general health and hospital treatments.
    """
    #
    #agent defination
    task_output= agent(str(input[0].parts[0].content))
    #
    yield Message(parts=[MessagePart(content=str(task_output))])

if __name__ == "__main__":
    server.run(port=8002)
