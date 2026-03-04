from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json
load_dotenv()
client = OpenAI()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
config = {
    "version":"v1.1",
    "embedder":{
        "provider":"openai",
        "config":{
           "api_key": OPEN_AI_API_KEY, "model": "text-embedding-3-small"
        }
    },
    "llm":{
        "provider":"openai",
        "config":{
           "api_key": OPEN_AI_API_KEY, "model": "gpt-4.1"
        }

    },
    "graph_store":{
        "provider":"neo4j",
        "config":{
            "url": os.getenv("NEO4J_URI"),
            "username": os.getenv("NEO4J_USERNAME"),
            "password": os.getenv("NEO4J_PASSWORD")
        }
    },
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host": "localhost",
            "port": 6333,
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("Enter a query:>> ")

    search_for_memeory = mem_client.search(user_id="harshal", query=user_query)


    memories = [
        f"ID: {mem.get('id')}, \n Memory: {mem.get('memory')}" for mem in search_for_memeory.get("results")
    ]

    System_prompt = f"""You are a helpful assistant. Below are some of the relevant memories retrieved based on the user query. Use them to answer the question. If you don't find any relevant memories, just answer based on your knowledge.    
    {json.dumps(memories)}
    """  

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": System_prompt},
            {"role": "user", "content": user_query}
        ]
    )   

    ai_response = response.choices[0].message.content
    print("\n\nAI Response:", ai_response)

    mem_client.add(user_id="harshal", messages=[
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": ai_response}
    ])

    print("\n\nMemory added successfully!")