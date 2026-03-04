from dotenv import load_dotenv
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.messages import SystemMessage
from langchain.chat_models import init_chat_model


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
    print("\n\nChatbot node called with state:", state)
    return {
        "messages": [ response],
    }

def sample_node(state: State):
    """A sample node that takes in messages and does something with them"""
    print("\n\nSample node called with state:", state)
    return {
        "messages": [ "Hi, this is a message for sample node"],
    }


graph_builder = StateGraph(State)

graph_builder.add_node("Chatbot",chatbot)
graph_builder.add_node("SampleNode",sample_node)

graph_builder.add_edge(START, "Chatbot")
graph_builder.add_edge("Chatbot", "SampleNode")
graph_builder.add_edge("SampleNode", END)

graph = graph_builder.compile()
updated_state = graph.invoke({ "messages": ["Hi, my name is Harshal"] })
print("\n\nUpdated state after graph execution:", updated_state)