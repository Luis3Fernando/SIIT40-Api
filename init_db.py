from app.core.database import engine
from app.models.base import Base
from app.models.user import User
from app.models.greenhouse import Greenhouse, Specie, Plant
from app.models.history import TelemetryHistory

def create_tables():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas con éxito!")

if __name__ == "__main__":
    create_tables()