from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Paiement(Base):
    __tablename__ = "paiement"

    id_paiement = Column(Integer, primary_key=True)
    date_paiement = Column(DateTime, default=datetime.utcnow)
    montant = Column(Float, nullable=False)
    methode = Column(String(50), nullable=False)  # carte, cash, paypal…
    statut = Column(String(30), default="en_attente")
    transaction_id = Column(String(100))

    id_commande = Column(Integer, ForeignKey("commande.id_commande"), unique=True, nullable=False)

    # Relation
    commande = relationship("Commande", back_populates="paiement")
