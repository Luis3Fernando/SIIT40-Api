import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Importamos para asegurar que los modelos se registren
import app.models 
from app.core.database import get_db
from app.models.greenhouse import Specie
from app.schemas.specie import SpecieOut

app = FastAPI(title="SIIT API - Tesis V1")

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/v1/specie", response_model=List[SpecieOut])
def get_all_species(db: Session = Depends(get_db)):
    """
    Lista todas las especies del catálogo. 
    Si la base de datos está vacía, devuelve [].
    """
    db_species = db.query(Specie).all()
    return db_species

@app.get("/api/v1/saludo")
def saludo_tesis(usuario: str = "Invitado"):
    return {
        "mensaje": f"Hola {usuario}, consulta realizada con éxito",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "proyecto": "SIIT40 - Sistema de Invernadero Automatizado",
        "estado": "Desarrollo"
    }