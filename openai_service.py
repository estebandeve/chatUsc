import openai
from config import OPENAI_API_KEY

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)  

def obtener_respuesta(pregunta):
    try:
        respuesta = openai_client.chat.completions.create( 
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un chatbot experto en consultas."},
                {"role": "user", "content": pregunta}
            ]
        )
        return respuesta.choices[0].message.content  
    except Exception as e:
        print(f"Error en OpenAI: {e}")
        return "Lo siento, no pude generar una respuesta en este momento."
