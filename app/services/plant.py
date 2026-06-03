from sqlalchemy.orm import Session
from app.models.greenhouse import Plant
from app.schemas.plant import PlantCreateDTO, PlantUpdateDTO

class PlantService:
    def create(self, db: Session, data: PlantCreateDTO):
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

    def get_by_greenhouse(self, db: Session, greenhouse_id: int):
        return db.query(Plant).filter(
            Plant.greenhouse_id == greenhouse_id,
            Plant.status == "active"
        ).all()

    def update(self, db: Session, plant_id: int, data: PlantUpdateDTO):
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if not plant:
            return {"error": "Planta no encontrada"}

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(plant, key, value)

        db.commit()
        db.refresh(plant)
        return plant

    def delete_logical(self, db: Session, plant_id: int):
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if not plant:
            return {"error": "Planta no encontrada"}

        plant.status = "removed"
        db.commit()
        db.refresh(plant)
        return {"success": True}

plant_service = PlantService()