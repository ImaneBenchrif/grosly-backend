from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Produit(Base):
    __tablename__ = "produit"

    id_produit = Column(Integer, primary_key=True)
    nom = Column(String(150), nullable=False)
    description = Column(String)
    prix = Column(Float, nullable=False)
    image = Column(String)
    stock = Column(Integer, default=0)
    origine = Column(String(100))
    condition = Column(String(100))
    poids = Column(Float)
    promotion = Column(Float, default=0)
    date_ajout = Column(Date)

    id_categorie = Column(Integer, ForeignKey("categorie.id_categorie"))

    categorie = relationship("Categorie", backref="produits")

    lignes_panier = relationship("LignePanier", back_populates="produit")
