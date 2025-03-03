import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Obtener la lista de asistentes
assistants = client.beta.assistants.list()

# Mostrar los asistentes disponibles
for assistant in assistants.data:
    print(f"ID: {assistant.id} - Nombre: {assistant.name}")
