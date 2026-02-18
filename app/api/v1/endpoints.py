import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.greenhouse import Specie
from app.schemas.specie import SpecieCreate, SpecieOut
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter()
UPLOAD_DIR = Path("static/assets")

@router.get("/api/v1/saludo")
def saludo_tesis(usuario: str = "Invitado"):
    return {
        "mensaje": f"Hola {usuario}, consulta realizada con éxito",
        "proyecto": "SIIT40 - Sistema de Invernadero Automatizado",
        "estado": "Desarrollo"
    }
  
@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=user_data.password 
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=UserOut)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_data.email, 
        User.password == user_data.password
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales incorrectas"
        )

    return user
    
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