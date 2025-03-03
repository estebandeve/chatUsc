import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

thread = client.beta.threads.create()

with open("thread_id.txt", "w") as f:
    f.write(thread.id)

print(f"Hilo creado con ID: {thread.id}")
