from sqlalchemy.orm import Session
from app.core.database import engine
from app.models.base import Base
from app.models.user import User
from app.models.greenhouse import Greenhouse
from app.core.security import SecurityUtils
from app.core.config import settings

def create_tables():
    Base.metadata.create_all(bind=engine)

def seed_data():
    db = Session(engine)
    try:
        admin_email = settings.SEED_ADMIN_EMAIL
        existing_user = db.query(User).filter(User.email == admin_email).first()
        
        if not existing_user:
            hashed_pw = SecurityUtils.hash_password(settings.SEED_ADMIN_PASSWORD)
            new_user = User(
                full_name="Luis Fernando Chumbes Ramos",
                email=admin_email,
                password=hashed_pw
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            new_gh = Greenhouse(
                user_id=new_user.id,
                name="Invernadero Inteligente con Tecnología 4.0",
                location="Lahuani, Challhuahuacho, Cotabambas, Apurímac",
                latitude=-14.194344,
                longitude=-72.353681
            )
            db.add(new_gh)
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_data()