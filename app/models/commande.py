from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Commande(Base):
    __tablename__ = "commande"

    id_commande = Column(Integer, primary_key=True)
    numero_commande = Column(String(50), unique=True, nullable=False)
    date_commande = Column(DateTime, default=datetime.utcnow)
    statut = Column(String(30), default="en_attente")
    montant_total = Column(Float, nullable=False)
    notes = Column(String)

    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)
    id_adresse = Column(Integer, ForeignKey("adresse.id_adresse"), nullable=False)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="commandes")
    lignes = relationship("LigneCommande", back_populates="commande", cascade="all, delete-orphan")
    adresse = relationship("Adresse", back_populates="commandes")
    paiement = relationship("Paiement", back_populates="commande", uselist=False)
    livraison = relationship("Livraison", back_populates="commande", uselist=False)


