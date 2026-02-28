from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv()
client = OpenAI(
    api_key="AIzaSyBfyGdHlkUV-PMF4iyWcmx0bxr2ozU1irM",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

response = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {"role" : "user", "content" : "hey there"}
    ]
)
print("response >>>>")
print(response)
print("response.choices[0] >>>>")
print(response.choices[0])
print("response.choices[0].message >>>>")
print(response.choices[0].message)
print("response.choices[0].message.content) >>>>")
print(response.choices[0].message.content)