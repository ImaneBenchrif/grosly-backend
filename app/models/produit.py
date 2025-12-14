from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid

from .base import Base


class Produit(Base):
    __tablename__ = "produit"

    id_produit = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nom = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    prix = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    image = Column(String, nullable=True)
    origine = Column(String(100), nullable=True)
    condition = Column(String(100), nullable=True)
    poids = Column(Float, nullable=True)

    promotion = Column(Float, nullable=True)  # % ou montant fixe

    date_creation = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    date_modification = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    id_categorie = Column(
        UUID(as_uuid=True),
        ForeignKey("categorie.id_categorie"),
        nullable=False
    )

    # Relations
    categorie = relationship("Categorie", back_populates="produits")
    lignes_panier = relationship("LignePanier", back_populates="produit")
