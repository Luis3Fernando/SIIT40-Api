from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.base_response import APIResponse
from app.schemas.specie import SpecieOutDTO, SpecieUpdateDTO
from app.services.specie import specie_service
from app.utils.response_helper import ResponseHelper

router = APIRouter()

@router.get("", response_model=APIResponse[List[SpecieOutDTO]])
def get_all_species(db: Session = Depends(get_db)):
    species = specie_service.get_all(db)
    return ResponseHelper.success(
        message="Lista de especies obtenida correctamente",
        data=species
    )

@router.post("", response_model=APIResponse[SpecieOutDTO])
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
    result = specie_service.create(db, name, scientific_name, color, vol, freq, raw, file)
    return ResponseHelper.success(
        message="Especie creada correctamente",
        data=result
    )

@router.patch("/{species_id}", response_model=APIResponse[SpecieOutDTO])
def update_specie(species_id: int, data: SpecieUpdateDTO, db: Session = Depends(get_db)):
    result = specie_service.update(db, species_id, data)
    if isinstance(result, dict) and "error" in result:
        return ResponseHelper.error(message=result["error"], msg_type="warning")
    return ResponseHelper.success(
        message="Especie actualizada correctamente",
        data=result
    )

@router.delete("/{species_id}", response_model=APIResponse)
def delete_specie(species_id: int, db: Session = Depends(get_db)):
    result = specie_service.delete(db, species_id)
    if "error" in result:
        return ResponseHelper.error(message=result["error"], msg_type="warning")
    return ResponseHelper.success(
        message="Especie eliminada correctamente"
    )