from sqlalchemy.orm import Session
from uuid import UUID
from app.models.greenhouse import Specie
from app.schemas.specie import SpecieCreateDTO, SpecieUpdateDTO

class SpecieService:
    def get_all(self, db: Session):
        return db.query(Specie).all()

    def create(self, db: Session, data: SpecieCreateDTO):
        new_specie = Specie(
            name=data.name,
            scientific_name=data.scientific_name,
            image_url=data.image_url,
            color=data.color,
            vol=data.vol,
            freq=data.freq,
            raw=data.raw
        )
        db.add(new_specie)
        db.commit()
        db.refresh(new_specie)
        return new_specie

    def update(self, db: Session, species_id: UUID, data: SpecieUpdateDTO):
        specie = db.query(Specie).filter(Specie.species_id == species_id).first()
        if not specie:
            return {"error": "Especie no encontrada"}

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(specie, key, value)

        db.commit()
        db.refresh(specie)
        return specie

    def delete(self, db: Session, species_id: UUID):
        specie = db.query(Specie).filter(Specie.species_id == species_id).first()
        if not specie:
            return {"error": "Especie no encontrada"}

        db.delete(specie)
        db.commit()
        return {"success": True}

specie_service = SpecieService()