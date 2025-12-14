from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid

from .base import Base


class Panier(Base):
    __tablename__ = "panier"

    id_panier = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    statut = Column(
        String(30),
        default="actif",
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

    id_utilisateur = Column(
        UUID(as_uuid=True),
        ForeignKey("utilisateur.id_utilisateur"),
        nullable=False
    )

    # Relations
    utilisateur = relationship(
        "Utilisateur",
        back_populates="panier"
    )

    lignes = relationship(
        "LignePanier",
        back_populates="panier",
        cascade="all, delete-orphan"
    )
