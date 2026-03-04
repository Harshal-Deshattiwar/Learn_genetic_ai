from dotenv import load_dotenv
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.messages import SystemMessage
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver


load_dotenv()

llm = init_chat_model(
    "gpt-4.1-mini",
    model_provider="openai",   
    temperature=0
)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def chatbot(state: State):
    """LLM decides whether to call a tool or not"""
    response = llm.invoke(state.get("messages"))
    # print("\n\nChatbot node called with state:", state)
    return {
        "messages": [ response],
    }



graph_builder = StateGraph(State)

graph_builder.add_node("Chatbot",chatbot)

graph_builder.add_edge(START, "Chatbot")
graph_builder.add_edge("Chatbot", END)

def comple_graph_with_checkpointer(checkpointer):
    return  graph_builder.compile(checkpointer=checkpointer)
   

DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = comple_graph_with_checkpointer(checkpointer=checkpointer)
    config = {
        "configurable": {
            "thread_id": "harshal",
        }
    }
    for chunk in graph_with_checkpointer.stream(State({ "messages": ["What is my name and what am I learning?"] }),config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()

    # print("\n\nUpdated state after graph execution:", updated_state)