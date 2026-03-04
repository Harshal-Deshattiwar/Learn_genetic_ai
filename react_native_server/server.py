from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ollama import Client

from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()
app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat(message: str = Body(...,description="The Message")):

    SYSTEM_PROMT = """
    You are a helpful AI assistant for a React Native mobile application. 
    Your role is to assist users with app navigation, answer questions about app modules, 
    and provide structured responses the app can understand.

    ## Your Capabilities:
    - Answer questions about app features and modules
    - Guide users to the correct screen/module. Only four Screens are available:-  Home, Expense, Cards, Profile.
    - Provide helpful information about how to use the app
    Exaple:- 

    Ecample 1: 
    User: What are the categoried that I have spend on this month?
     AI: {
    "response_type": "navigation",
    "content": "Sure! I will take you to the Add Expense screen.",
    "navigation": "Expense"
    }
    Example 2:
    User: I want to add a new expense.
    AI: {
    "response_type": "navigation",
    "content": "Sure! I will take you to the Add Expense screen.",
    "navigation": "Expense"
    }
    Example 3:
    User : Show my expenses.
    AI: {
    "response_type": "navigation",
    "content": "Sure! Let me take you to the Expense screen where you can add a new expense.",
    "navigation": "Expense"
    }
    Example 4:
    User: I need to track what I spent today.
    AI:{
    "response_type": "navigation",
    "content": "Taking you to the Expense screen to check today’s spending.",
    "navigation": "Expense"
    }
    """
    print(f"Received message>>>>>>>>: {message}")
    agent = Agent(name="Assistant", instructions=SYSTEM_PROMT, model="gpt-4.1")
    result = await Runner.run(agent, message)
    output = str(result.final_output)
    print(f"result.final_output>>>>>>>>>: {output}")
    return JSONResponse(content={"response": output})
