import os
from crewai_tools import RagTool
from dotenv import load_dotenv
load_dotenv()

class CrewTools:
    def __init__(self):
        return
    
    def rag_tool(self, config=None):
        if config is None:
            config = {
                "llm": {
                    "provider": "google",
                    "config": {
                        "model": "gemini-2.5-flash",
                        "api_key": os.getenv("GOOGLE_API_KEY"),
                    }
                },
                "embedding_model": {
                    "provider": "ollama",
                    "config": {
                        "model": "all-minilm:latest",
                    }
                }
            }
        return RagTool(config=config)