from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class LignePanier(Base):
    __tablename__ = "ligne_panier"

    id_panier = Column(Integer, ForeignKey("panier.id_panier"), primary_key=True)
    id_produit = Column(Integer, ForeignKey("produit.id_produit"), primary_key=True)

    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)

    # Relations
    panier = relationship("Panier", back_populates="lignes")
    produit = relationship("Produit")
