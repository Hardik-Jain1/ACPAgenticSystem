from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Server, Context, RunYield, RunYieldResume

from crewai import Crew, Task, Agent, LLM
from crewai_tools import RagTool
import os
from dotenv import load_dotenv
load_dotenv()

server = Server()

class PolicyCrew:
    def __init__(self, input_text: str):
        self.llm = LLM(model="gemini/gemini-2.5-flash",
                        api_key=os.getenv("GOOGLE_API_KEY"),
                        #   base_url="http://localhost:11434",
                        temperature=0.5,
                        max_tokens=4096)
        self.config = {
            "llm": {
                "provider": "google",
                "config": {
                    "model": "gemini-2.5-flash",
                    # "api_key": os.getenv("GOOGLE_API_KEY"),
                }
            },
            "embedding_model": {
                "provider": "ollama",
                "config": {
                    "model": "all-minilm:latest",
                }
            }
        }
        self.rag_tool = RagTool(config=self.config)
        self.rag_tool.add("./data/gold-hospital-and-premium-extras.pdf", data_type="pdf_file")

        self.insurance_agent = Agent(
            role="Senior Insurance Coverage Assistant",
            goal="Determine whether something is covered or not",
            backstory="You are an expert insurance agent designed to assist with coverage queries.",
            llm=self.llm,
            tools=[self.rag_tool],
            max_retry_limit=5,
            allow_delegation=False,
            verbose=True
        )

        self.insurance_task = Task(
            description=input_text,
            expected_output="A comprehensive response as to the users question",
            agent=self.insurance_agent
        )

        self.crew = Crew(
            agents=[self.insurance_agent],
            tasks=[self.insurance_task],
            verbose=True
        )
    
    async def run(self):
        task_output = await self.crew.kickoff_async()
        return task_output

@server.agent()
async def policy_agent(input: list[Message],
                       context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is an agent for questions around policy coverage, it uses a RAG pattern to find answers based on policy documentation. Use it to help answer questions on coverage and waiting periods."""
    #
    #agent defination
    input_text = input[0].parts[0].content if input else "What is the waiting period for rehabilitation?"
    policy_crew = PolicyCrew(input_text)
    task_output = await policy_crew.run()
    #
    yield Message(parts=[MessagePart(content=str(task_output))])

if __name__ == "__main__":
    server.run(port=8001)
    