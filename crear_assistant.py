import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

assistant = client.beta.assistants.create(
    name="Consultor de Presupuestos",
    instructions="Responde solo con la información del archivo adjunto. Si no encuentras la respuesta en el archivo, di que no puedes ayudar.",
    model="gpt-4-turbo",
    tools=[{"type": "file_search"}]
)

print(f"✅ Assistant creado con ID: {assistant.id}")

