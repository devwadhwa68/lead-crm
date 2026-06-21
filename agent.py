from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
search = DuckDuckGoSearchRun()

def research_agent(query):
    print(f"\nSearching for: {query}")
    search_result = search.run(query)
    
    prompt = f"""Based on this search result, answer the question clearly:
    
Search Result: {search_result}

Question: {query}

Give a clear, concise answer:"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

print("AI Research Agent ready! Type 'exit' to quit.\n")
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    result = research_agent(query)
    print(f"\nAgent: {result}\n")