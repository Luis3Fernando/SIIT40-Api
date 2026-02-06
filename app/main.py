from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="SIIT API - Tesis V1")

@app.get("/api/v1/saludo")
def saludo_tesis(usuario: str = "Invitado"):
    return {
        "mensaje": f"Hola {usuario}, consulta realizada con éxito",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "proyecto": "SIIT40 - Sistema de Invernadero Automatizado",
        "estado": "Desarrollo."
    }