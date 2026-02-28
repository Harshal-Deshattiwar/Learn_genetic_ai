from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model='gpt-4.1-mini',
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