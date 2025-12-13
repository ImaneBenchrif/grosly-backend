from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Panier(Base):
    __tablename__ = "panier"

    id_panier = Column(Integer, primary_key=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    statut = Column(String(30), default="actif")

    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="panier")
    lignes = relationship("LignePanier", back_populates="panier", cascade="all, delete-orphan")
