from dotenv import load_dotenv
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.messages import SystemMessage
from langchain.chat_models import init_chat_model
from typing import Optional, Literal
from openai import OpenAI

load_dotenv()

client = OpenAI()

llm = init_chat_model(
    "gpt-4.1-mini",
    model_provider="openai",   
    temperature=0
)

class State(TypedDict):
    user_query: str
    llm_output : Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("\n\nChatbot node called with state:", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who answers user query."},
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state

def evaluation_response(state:State):
    print("\n\nEvaluation node called with state:", state)
    if True:
        return END
    return "chatbot_gemini"

def chatbot_gemini(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("\n\nChatbot Gemini node called with state:", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who answers user query."},
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state

def endnode(state: State):
    print("\n\nEndnode called with state:", state)
    print("\n\nFinal LLM Output:", state.get("llm_output"))
    return state
 

graph_builder = StateGraph(State)

graph_builder.add_node("Chatbot",chatbot)
graph_builder.add_node("evaluation_response",evaluation_response)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)

graph_builder.add_edge(START, "Chatbot")
graph_builder.add_conditional_edges("Chatbot", evaluation_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph= graph_builder.compile()
updated_state = graph.invoke({ "user_query": "What is the capital of France?" })
print("\n\nUpdated state after graph execution:", updated_state)
