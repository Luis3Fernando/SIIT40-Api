from app.core.database import SessionLocal
from app.models.greenhouse import Specie

def seed_species():
    db = SessionLocal()
    try:
        species_data = [
            {
                "name": "Tomate",
                "scientific_name": "Solanum lycopersicum",
                "image_url": "/static/assets/tomate.png",
                "color": "#FF5733",
                "vol": 1.5,
                "freq": 6,
                "raw": 2800
            },
            {
                "name": "Albahaca",
                "scientific_name": "Ocimum basilicum",
                "image_url": "/static/assets//albahaca.png",
                "color": "#2ECC71",
                "vol": 0.8,
                "freq": 12,
                "raw": 2200
            },
            {
                "name": "Lechuga",
                "scientific_name": "Lactuca sativa",
                "image_url": "/static/assets/lechuga.png",
                "color": "#82E0AA",
                "vol": 1.0,
                "freq": 8,
                "raw": 2500
            },
            {
                "name": "Espinaca",
                "scientific_name": "Spinacia oleracea",
                "image_url": "/static/assets/espinaca.png",
                "color": "#1D8348",
                "vol": 0.5,
                "freq": 24,
                "raw": 3000
            },
            {
                "name": "Menta",
                "scientific_name": "Mentha",
                "image_url": "/static/assets/menta.png",
                "color": "#58D68D",
                "vol": 1.2,
                "freq": 4,
                "raw": 2100
            }
        ]
        
        for data in species_data:
            exists = db.query(Specie).filter(Specie.name == data["name"]).first()
            if not exists:
                new_specie = Specie(**data)
                db.add(new_specie)
        
        db.commit()
        print("¡Catálogo de especies listo!")

    except Exception as e:
        print(f"Error al sembrar: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_species()