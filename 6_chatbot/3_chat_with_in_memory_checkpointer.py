from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

memory = MemorySaver()

llm = ChatGroq(model="llama-3.1-8b-instant")

class BasicChatState(TypedDict): 
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState): 
    return {
       "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)

graph.add_edge("chatbot", END)

graph.set_entry_point("chatbot")

app = graph.compile(checkpointer=memory)

config = {"configurable": {
    "thread_id": 1
}}

while True: 
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)

        print("AI: " + result["messages"][-1].content)


# response1 = app.invoke({
#     "messages": HumanMessage(content="Hi, I'm Vijay")
# }, config=config)

# response2 = app.invoke({
#     "messages": HumanMessage(content="What is my name?")
# }, config=config)

# print(response1)
# print("\n")
# print(config)
# print("\n")
# print(response2)