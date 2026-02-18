from datetime import datetime
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.greenhouse import Specie
from app.schemas.specie import SpecieCreate, SpecieOut
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.models.greenhouse import Greenhouse, Plant, Specie
from app.schemas.greenhouse import GreenhouseCreate, GreenhouseOut
from app.schemas.plant import PlantCreate, PlantUpdate, PlantOut
from app.models.history import TelemetryHistory
from app.schemas.history import LocalBackupLog

router = APIRouter()
UPLOAD_DIR = Path("static/assets")

@router.get("/saludo")
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
  
@router.post("/greenhouse", response_model=GreenhouseOut)
def create_greenhouse(data: GreenhouseCreate, db: Session = Depends(get_db)):
    new_gh = Greenhouse(
        name=data.name,
        location=data.location,
        latitude=data.latitude,
        longitude=data.longitude,
        user_id=data.userId
    )
    db.add(new_gh)
    db.commit()
    db.refresh(new_gh)
    return new_gh

@router.get("/greenhouse/{gh_id}", response_model=GreenhouseOut)
def get_greenhouse_info(gh_id: int, db: Session = Depends(get_db)):
    gh = db.query(Greenhouse).filter(Greenhouse.id == gh_id).first()
    
    if not gh:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    
    count = db.query(Plant).filter(Plant.greenhouse_id == gh_id).count()
    gh.plant_count = count
    return gh

@router.post("/plant", response_model=PlantOut)
def create_plant(data: PlantCreate, db: Session = Depends(get_db)):
    new_plant = Plant(
        greenhouse_id=data.greenhouse_id,
        species_id=data.species_id,
        zone=data.zone,
        stage=data.stage,
        count=data.count
    )
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant

@router.get("/plant/me/{gh_id}", response_model=List[PlantOut])
def get_my_plants(gh_id: int, db: Session = Depends(get_db)):
    plants = db.query(Plant).filter(Plant.greenhouse_id == gh_id).all()
    return plants

@router.patch("/plant/{plant_id}", response_model=PlantOut)
def update_plant(plant_id: int, data: PlantUpdate, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(status_code=404, detail="Planta no encontrada")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plant, key, value)
    
    db.commit()
    db.refresh(db_plant)
    return db_plant
 
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

from app.models.history import TelemetryHistory
from app.schemas.history import LocalBackupLog

@router.post("/history/upload")
def upload_telemetry(log: LocalBackupLog, db: Session = Depends(get_db)):
    history_entries = []
    
    for entry in log.data:
        new_record = TelemetryHistory(
            greenhouse_id=1,
            nodo_id=entry.Nodo_ID,
            file_name=log.fileName,
            recorded_at=datetime.fromisoformat(entry.TS.replace("Z", "+00:00")),
            sd_status_pct=entry.Sistema.Memoria_SD_Pct,
            soil_raw=entry.Metricas_Ambientales.Suelo_RAW,
            temp_c=entry.Metricas_Ambientales.Temp_C,
            hum_pct=entry.Metricas_Ambientales.Hum_Pct,
            ph=entry.Metricas_Ambientales.pH,
            co2=entry.Metricas_Ambientales.CO2,
            lux=entry.Metricas_Ambientales.Lux,
            flow_lmin=entry.Metricas_Agua.Lmin,
            total_l=entry.Metricas_Agua.Total_L,
            valve_open=bool(entry.Estado_Actuadores.Valvula),
            is_manual=bool(entry.Estado_Actuadores.Manual)
        )
        history_entries.append(new_record)
    
    db.add_all(history_entries)
    db.commit()
    return {"status": "success", "records_uploaded": len(history_entries)}

@router.get("/history/stats/{nodo_id}")
def get_node_stats(nodo_id: str, db: Session = Depends(get_db)):
    stats = db.query(
        func.avg(TelemetryHistory.temp_c).label("avg_temp"),
        func.avg(TelemetryHistory.hum_pct).label("avg_hum"),
        func.avg(TelemetryHistory.ph).label("avg_ph"),
        func.max(TelemetryHistory.total_l).label("total_water")
    ).filter(TelemetryHistory.nodo_id == nodo_id).first()
    
    return {
        "nodo": nodo_id,
        "temp_promedio": round(stats.avg_temp or 0, 2),
        "humedad_promedio": round(stats.avg_hum or 0, 2),
        "ph_promedio": round(stats.avg_ph or 0, 2),
        "consumo_total_agua": stats.total_water or 0
    }