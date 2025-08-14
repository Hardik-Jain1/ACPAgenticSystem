from crewai import Task

class CrewTasks:
    def __init__(self):
        return
    
    def insurance_task(self, agent):
        return Task(
            description="What is the waiting period for rehabilitation?",
            expected_output="A comprehensive response as to the users question",
            agent=agent
        )