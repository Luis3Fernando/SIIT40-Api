import datetime
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.greenhouse import Specie
from app.schemas.specie import SpecieOut
from fastapi.staticfiles import StaticFiles
import os
from typing import List

app = FastAPI(title="SIIT API - Tesis V1")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/v1/specie", response_model=List[SpecieOut])
def get_all_species(db: Session = Depends(get_db)):
    db_species = db.query(Specie).all()
    return db_species

@app.get("/api/v1/saludo")
def saludo_tesis(usuario: str = "Invitado"):
    return {
        "mensaje": f"Hola {usuario}, consulta realizada con éxito",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "proyecto": "SIIT40 - Sistema de Invernadero Automatizado",
        "estado": "Desarrollo."
    }