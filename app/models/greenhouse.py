from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class Greenhouse(Base):
    __tablename__ = "greenhouse"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String)
    location = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")

class Specie(Base):
    __tablename__ = "specie"

    species_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=False)
    image_url = Column(String)
    color = Column(String)
    vol = Column(Float)
    freq = Column(Integer)
    raw = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

class Plant(Base):
    __tablename__ = "plant"

    id = Column(Integer, primary_key=True, index=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"))
    species_id = Column(Integer, ForeignKey("specie.species_id"))
    zone = Column(String)
    stage = Column(String)
    count = Column(Integer, default=1)
    is_critical = Column(Boolean, default=False)
    last_watered = Column(DateTime, nullable=True)
    status = Column(String, default="active")
    planted_at = Column(DateTime, server_default=func.now())
    specie = relationship("Specie")
    greenhouse = relationship("Greenhouse")