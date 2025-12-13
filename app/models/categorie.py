from sqlalchemy import Column, Integer, String, Text
from .base import Base


class Categorie(Base):
    __tablename__ = "categorie"

    id_categorie = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    image = Column(String)
    description = Column(Text)
