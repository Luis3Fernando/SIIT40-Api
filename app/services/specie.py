import shutil
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.greenhouse import Specie
from app.schemas.specie import SpecieUpdateDTO

UPLOAD_DIR = Path("static/assets")

class SpecieService:
    def get_all(self, db: Session):
        return db.query(Specie).all()

    def create(self, db: Session, name: str, scientific_name: str, color: str, vol: float, freq: int, raw: float, file: UploadFile):
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = f"/static/assets/{unique_filename}"

        new_specie = Specie(
            name=name,
            scientific_name=scientific_name,
            image_url=image_url,
            color=color,
            vol=vol,
            freq=freq,
            raw=raw
        )
        db.add(new_specie)
        db.commit()
        db.refresh(new_specie)
        return new_specie

    def update(self, db: Session, species_id: int, data: SpecieUpdateDTO):
        specie = db.query(Specie).filter(Specie.species_id == species_id).first()
        if not specie:
            return {"error": "Especie no encontrada"}

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(specie, key, value)

        db.commit()
        db.refresh(specie)
        return specie

    def delete(self, db: Session, species_id: int):
        specie = db.query(Specie).filter(Specie.species_id == species_id).first()
        if not specie:
            return {"error": "Especie no encontrada"}

        db.delete(specie)
        db.commit()
        return {"success": True}

specie_service = SpecieService()