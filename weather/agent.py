from dotenv import load_dotenv
from openai import OpenAI
import requests
import json


load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    for every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The correct sequence of steps is: START (where the user gives an input) → PLAN (can be repeated multiple times for reasoning and preparation) → TOOL (only when an external tool needs to be called and we wait for its observation) → OUTPUT (final answer returned to the user)."
    
    Output JSON Format: {"step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input" : "string" }
    Available Tools:
    - get_weather(city: str): Takes city name as an input string and returns the weather info about the city.

    Example 1 — Weather query (uses TOOL)
    START: {"step":"START","content":"What is the weather in Goa?"}

    PLAN: {"step":"PLAN","content":"The user wants weather information for a city. I should call the get_weather tool with city = Goa."}
    PLAN: {"step": "TOOL": "tool": "get_weather", "input": "delhi" }
    PLAN: {"step": "OBSERVE": "tool": "get_weather", "output": "The temp of delhi is cloudy with 20
    PLAN: {"step":"TOOL","content":"get_weather(city='Goa')"}

    OUTPUT: {"step":"OUTPUT","content":"Here is the current weather information for Goa."}

    Example 2 — General question (no tool required)
    START: {"step":"START","content":"Explain what REST API means in simple words."}

    PLAN: {"step":"PLAN","content":"The user wants a simple explanation of REST API. No external tool is required. I should prepare a short and clear explanation."}

    OUTPUT: {"step":"OUTPUT","content":"A REST API is a way for two software systems to talk to each other over the internet using simple HTTP requests like GET, POST, PUT and DELETE."}

    Example 3 — Missing information case
    START: {"step":"START","content":"Get weather information."}

    PLAN: {"step":"PLAN","content":"The user did not specify the city. I should ask the user for the city name before calling the get_weather tool."}

    OUTPUT :{"step":"OUTPUT","content":"Please tell me the city name for which you want the weather information."}



"""





def get_Weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"

    headers = {
        "User-Agent": "curl/7.88.1"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"

        return "Weather service returned error"

    except requests.exceptions.RequestException as e:
        return f"Weather service not reachable: {e}"

available_tools = {
    "get_weather": get_Weather,
}


def main():

    user_input = input("> ")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    while True:

        response = client.chat.completions.parse(
            model='gpt-4.1-mini',
            response_format={"type": "json_object"},
            messages=messages
        )

        raw = response.choices[0].message.content
        step_obj = json.loads(raw)

        step = step_obj.get("step", "")
        content = step_obj.get("content", "")
        tool = step_obj.get("tool", "")
        tool_input = step_obj.get("input", "")

        # -------------------------
        # START
        # -------------------------
        if step == "START":
            print("\n🟢 START")
            print(content)

        # -------------------------
        # PLAN
        # -------------------------
        elif step == "PLAN":
            print("\n🧠 PLAN")
            print(content)

        # -------------------------
        # TOOL
        # -------------------------
        elif step == "TOOL":
            print("\n🛠️ TOOL")
            print(content)

            print(f"👉 Using tool: {tool}")
            print(f"👉 Tool input: {tool_input}")

        # -------------------------
        # OUTPUT
        # -------------------------
        elif step == "OUTPUT":
            print("\n✅ OUTPUT")
            print(content)

        else:
            print("\n⚠️ Unknown step")
            print(step_obj)

        # always store assistant message
        messages.append(
            {"role": "assistant", "content": raw}
        )

        # stop when OUTPUT is produced
        if step == "OUTPUT":
            break

        # if TOOL step, run tool and send observation
        if step == "TOOL":

            if tool in available_tools:
                tool_output = available_tools[tool](tool_input)
            else:
                tool_output = f"Tool '{tool}' not found."

            print("\n🔎 OBSERVATION")
            print(tool_output)

            messages.append(
                {
                    "role": "user",
                    "content": f"OBSERVATION: {tool_output}"
                }
            )



main()
