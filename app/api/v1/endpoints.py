import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.greenhouse import Specie
from app.schemas.specie import SpecieCreate, SpecieOut

router = APIRouter()
UPLOAD_DIR = Path("static/assets")

@router.get("/api/v1/saludo")
def saludo_tesis(usuario: str = "Invitado"):
    return {
        "mensaje": f"Hola {usuario}, consulta realizada con éxito",
        "proyecto": "SIIT40 - Sistema de Invernadero Automatizado",
        "estado": "Desarrollo"
    }
    
@router.get("/specie", response_model=List[SpecieOut])
def get_species(db: Session = Depends(get_db)):
    return db.query(Specie).all()


@router.post("/specie", response_model=SpecieOut)
def create_specie(
    name: str = Form(...),
    scientific_name: str = Form(...),
    color: str = Form(...),
    vol: float = Form(...),
    freq: int = Form(...),
    raw: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_image_url = f"/static/assets/{unique_filename}"
    
    new_specie = Specie(
        name=name,
        scientific_name=scientific_name,
        image_url=db_image_url,
        color=color,
        vol=vol,
        freq=freq,
        raw=raw
    )
    
    db.add(new_specie)
    db.commit()
    db.refresh(new_specie)
    return new_specie