import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

ASSISTANT_ID = "asst_rSJkXjpasVcpx6oVYXJ1Ke1S"

app = FastAPI()

class ChatRequest(BaseModel):
    pregunta: str


# se buscan los archivos que subi a OpenAI
def listar_archivos():
    response = client.files.list()
    archivos = [file.id for file in response.data if file.purpose == "assistants"]
    print(f"Archivos disponibles: {archivos}")
    return archivos



# se crea un vector el cual va a tener el conocimiento de los archivos subido por el usuario 
def crear_vector():
    response = client.beta.vector_stores.create(name="Base de Conocimiento")
    vector_store_id = response.id
    print(f" Vector Store creada: {vector_store_id}")
    return vector_store_id



# Se agrega el archivo al vector
def agregar_archivos_a_vector(vector_store_id, archivos_subidos):
    client.beta.vector_stores.file_batches.create_and_poll(vector_store_id, file_ids=archivos_subidos)
    print(f"Archivos {archivos_subidos} agregados a Vector Store {vector_store_id}")



# Se vincula el vector osea la base de datos al asitente 
def actualizar_asistente_con_vector_store(vector_store_id):
    response = client.beta.assistants.update(
        assistant_id=ASSISTANT_ID,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
    )
    print(f"Asistente actualizado con Vector Store: {vector_store_id}")



# se empieza a ejecutar las funciones 
archivos_subidos = listar_archivos()  
if archivos_subidos:
    vector_id = crear_vector() 
    agregar_archivos_a_vector(vector_id, archivos_subidos)  
    actualizar_asistente_con_vector_store(vector_id)  
else:
    print(" No hay archivos disponibles. Sube archivos primero.")

# Se ejecuta la accion para el chat
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Crear mensaje del usuario
        message = client.beta.threads.messages.create(
            thread_id="thread_qkBph8stNiMYeF38pgPM08Fe",
            role="user",
            content=request.pregunta
        )

        # Ejecutar la consulta en el asistente
        run = client.beta.threads.runs.create(
            thread_id="thread_qkBph8stNiMYeF38pgPM08Fe",
            assistant_id=ASSISTANT_ID
        )

        # Esperar respuesta
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id="thread_qkBph8stNiMYeF38pgPM08Fe", run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)  # Espera 1 segundo antes de volver a verificar

        # Obtener respuesta del asistente
        messages = client.beta.threads.messages.list(thread_id="thread_qkBph8stNiMYeF38pgPM08Fe")
        respuesta = messages.data[0].content[0].text.value

        return {"respuesta": respuesta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
