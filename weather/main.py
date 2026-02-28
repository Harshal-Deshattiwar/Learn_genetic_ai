from dotenv import load_dotenv
from openai import OpenAI
import requests



# load_dotenv()
client = OpenAI(
    api_key="AIzaSyDN22H0ut115w1p8nF3YCvSy4sYt8dZY6I",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

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



def main():
    userQuery = input(">")
    response = client.chat.completions.create(
        model='gemini-2.5-flash',
        messages=[
            {"role" : "user", "content" : userQuery}
        ]
    )
    print(f":> {response.choices[0].message.content}")

print(get_Weather("goa"))
