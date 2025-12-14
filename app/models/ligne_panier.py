from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .base import Base


class LignePanier(Base):
    __tablename__ = "ligne_panier"

    id_panier = Column(
        UUID(as_uuid=True),
        ForeignKey("panier.id_panier"),
        primary_key=True
    )

    id_produit = Column(
        UUID(as_uuid=True),
        ForeignKey("produit.id_produit"),
        primary_key=True
    )

    quantite = Column(
        Integer,
        nullable=False
    )

    prix_unitaire = Column(
        Float,
        nullable=False
    )

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

    __table_args__ = (
        CheckConstraint("quantite > 0", name="check_quantite_positive"),
    )

    # Relations
    panier = relationship(
        "Panier",
        back_populates="lignes"
    )

    produit = relationship(
        "Produit",
        back_populates="lignes_panier"
    )
