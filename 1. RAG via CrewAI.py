from crewai import Crew, Agent, Task, LLM
from crewai_tools import RagTool

import os
from dotenv import load_dotenv
load_dotenv()

llm = LLM(model="gemini/gemini-2.5-flash",
          api_key=os.getenv("GOOGLE_API_KEY"),
        #   base_url="http://localhost:11434",
          temperature=0.5,
          max_tokens=4096)

config = {
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

rag_tool = RagTool(config=config)
rag_tool.add("./data/gold-hospital-and-premium-extras.pdf", data_type="pdf_file")

insurance_agent = Agent(
    role="Senior Insurance Coverage Assistant",
    goal="Determine whether something is covered or not",
    backstory= "You are an expert insurance agent designed to assist with coverage queries.",
    llm=llm,
    tools=[rag_tool],
    max_retry_limit=5,
    allow_delegation=False,
    verbose=True
)

task1 = Task(
    description="What is the waiting period for rehabilitation?",
    expected_output="A comprehensive response as to the users question",
    agent=insurance_agent
)

crew = Crew(
    agents=[insurance_agent],
    tasks=[task1],
    verbose=True
)

task_output = crew.kickoff()

print("Final Output: \n", task_output)