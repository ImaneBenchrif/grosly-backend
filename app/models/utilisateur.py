from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telephone = Column(String(30), unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    role = Column(String(50), default="user")
    is_verified = Column(Boolean, default=False)
    

    # Relations
    panier = relationship("Panier", back_populates="utilisateur", uselist=False)
    commandes = relationship("Commande", back_populates="utilisateur")
    adresses = relationship("Adresse", back_populates="utilisateur")

