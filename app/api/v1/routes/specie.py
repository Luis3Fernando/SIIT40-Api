from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.base_response import APIResponse
from app.schemas.specie import SpecieOutDTO, SpecieCreateDTO, SpecieUpdateDTO
from app.services.specie import specie_service
from app.utils.response_helper import ResponseHelper

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("", response_model=APIResponse[List[SpecieOutDTO]])
def get_all_species(db: Session = Depends(get_db)):
    species = specie_service.get_all(db)
    return ResponseHelper.success(
        message="Lista de especies obtenida correctamente",
        data=species
    )

@router.post("", response_model=APIResponse[SpecieOutDTO])
def create_specie(data: SpecieCreateDTO, db: Session = Depends(get_db)):
    result = specie_service.create(db, data)
    return ResponseHelper.success(
        message="Especie creada correctamente",
        data=result
    )

@router.patch("/{species_id}", response_model=APIResponse[SpecieOutDTO])
def update_specie(species_id: UUID, data: SpecieUpdateDTO, db: Session = Depends(get_db)):
    result = specie_service.update(db, species_id, data)
    if isinstance(result, dict) and "error" in result:
        return ResponseHelper.error(message=result["error"], msg_type="warning")
    return ResponseHelper.success(
        message="Especie actualizada correctamente",
        data=result
    )

@router.delete("/{species_id}", response_model=APIResponse)
def delete_specie(species_id: UUID, db: Session = Depends(get_db)):
    result = specie_service.delete(db, species_id)
    if "error" in result:
        return ResponseHelper.error(message=result["error"], msg_type="warning")
    return ResponseHelper.success(
        message="Especie eliminada correctamente"
    )