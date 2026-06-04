from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.base_response import APIResponse
from app.schemas.plant import PlantOutDTO, PlantCreateDTO, PlantUpdateDTO
from app.services.plant import plant_service
from app.utils.response_helper import ResponseHelper

router = APIRouter()

@router.post("", response_model=APIResponse[PlantOutDTO])
def create_plant(data: PlantCreateDTO, db: Session = Depends(get_db)):
    result = plant_service.create(db, data)
    return ResponseHelper.success(
        message="Planta registrada con éxito en el invernadero",
        data=result
    )

@router.get("/greenhouse/{gh_id}", response_model=APIResponse[List[PlantOutDTO]])
def get_plants_by_greenhouse(gh_id: int, db: Session = Depends(get_db)):
    plants = plant_service.get_by_greenhouse(db, gh_id)
    return ResponseHelper.success(
        message="Plantas del invernadero obtenidas correctamente",
        data=plants
    )

@router.patch("/{plant_id}", response_model=APIResponse[PlantOutDTO])
def update_plant(plant_id: int, data: PlantUpdateDTO, db: Session = Depends(get_db)):
    result = plant_service.update(db, plant_id, data)
    if isinstance(result, dict) and "error" in result:
        return ResponseHelper.error(message=result["error"], msg_type="warning")
    return ResponseHelper.success(
        message="Datos de la planta actualizados correctamente",
        data=result
    )

@router.delete("/{plant_id}", response_model=APIResponse)
def remove_plant(plant_id: int, db: Session = Depends(get_db)):
    result = plant_service.delete_logical(db, plant_id)
    if "error" in result:
        return ResponseHelper.error(message=result["error"], msg_type="warning")
    return ResponseHelper.success(
        message="Planta dada de baja correctamente del invernadero"
    )