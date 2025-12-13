from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Livraison(Base):
    __tablename__ = "livraison"

    id_livraison = Column(Integer, primary_key=True)
    type_livraison = Column(String(50), nullable=False)  # standard, express
    statut = Column(String(30), default="en_preparation")
    numero_suivi = Column(String(100))
    duree_estimee = Column(String(50))

    date_livraison_prevue = Column(DateTime)
    date_livraison_reelle = Column(DateTime)

    id_commande = Column(Integer, ForeignKey("commande.id_commande"), unique=True, nullable=False)

    # Relation
    commande = relationship("Commande", back_populates="livraison")
