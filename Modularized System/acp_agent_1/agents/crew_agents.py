import os
from crewai import Agent, LLM
from tools.crew_tools import CrewTools
from dotenv import load_dotenv
load_dotenv()
import json
with open("config.json", "r") as f:
    config = json.load(f)

class CrewAgents:
    def __init__(self):
        self.llm = LLM(**config["llm"]["config"])
        self.rag_tool = CrewTools().rag_tool(config["rag_tool_config"])
        self.rag_tool.add("./data/gold-hospital-and-premium-extras.pdf", data_type="pdf_file")

    
    def insurance_agent(self):
        return Agent(
            role="Senior Insurance Coverage Assistant",
            goal="Determine whether something is covered or not",
            backstory= "You are an expert insurance agent designed to assist with coverage queries.",
            llm=self.llm,
            tools=[self.rag_tool],
            max_retry_limit=5,
            allow_delegation=False,
            verbose=True
        )

