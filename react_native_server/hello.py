from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()
agent = Agent(name="Assistant", instructions="You are a helpful assistant which greets user and helps them answer questions using emoji and in a funny way")

result = Runner.run_sync(agent, "Hey, There my name is Harshal!")

print(result.final_output)