from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Adresse(Base):
    __tablename__ = "adresse"

    id_adresse = Column(Integer, primary_key=True)
    rue = Column(String(200), nullable=False)
    ville = Column(String(100), nullable=False)
    code_postal = Column(String(20), nullable=False)
    pays = Column(String(100), nullable=False)

    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="adresses")
    commandes = relationship("Commande", back_populates="adresse")
