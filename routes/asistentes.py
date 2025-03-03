from fastapi import FastAPI
from database import get_tablas, get_asistentes

app = FastAPI()

@app.get("/tablas")
def obtener_tablas():
    tablas = get_tablas()
    return {"tablas": tablas}

    @app.get("/asistentes")
def obtener_asistentes():
    asistentes = get_asistentes()
    return {"asistentes": asistentes}
