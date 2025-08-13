from crewai import Crew
from agents.crew_agents import CrewAgents
from tasks.crew_tasks import CrewTasks

class RAGCrew:
    def __init__(self):
        agents= CrewAgents()
        self.insurance_agent= agents.insurance_agent()

        tasks= CrewTasks()
        self.insurance_task= tasks.insurance_task(self.insurance_agent)

        self.crew= Crew(
            agents= [self.insurance_agent],
            tasks= [self.insurance_task],
            verbose=True
        )

    def run(self):
        return self.crew.kickoff()
    
    async def run_async(self):
        return await self.crew.kickoff_async()