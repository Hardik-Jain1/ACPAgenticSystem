from agent_1.crews.rag_crew import RAGCrew

def main():
    rag_crew= RAGCrew()
    output= rag_crew.run()
    print("Final Crew Output:\n", output)


if __name__=="__main__":
    main()

