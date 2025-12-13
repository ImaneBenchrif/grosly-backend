from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class LigneCommande(Base):
    __tablename__ = "ligne_commande"

    id_commande = Column(Integer, ForeignKey("commande.id_commande"), primary_key=True)
    id_produit = Column(Integer, ForeignKey("produit.id_produit"), primary_key=True)

    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)

    # Relations
    commande = relationship("Commande", back_populates="lignes")
    produit = relationship("Produit")
