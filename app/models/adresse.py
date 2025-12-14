from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid

from .base import Base


class Adresse(Base):
    __tablename__ = "adresse"

    id_adresse = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    label = Column(
        String(50),
        nullable=True
    )  # ex: Domicile, Travail

    rue = Column(
        String(200),
        nullable=False
    )

    ville = Column(
        String(100),
        nullable=False
    )

    code_postal = Column(
        String(20),
        nullable=False
    )

    pays = Column(
        String(100),
        nullable=False
    )

    is_default = Column(
        Boolean,
        default=False,
        nullable=False
    )

    id_utilisateur = Column(
        UUID(as_uuid=True),
        ForeignKey("utilisateur.id_utilisateur"),
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

    # Relations
    utilisateur = relationship(
        "Utilisateur",
        back_populates="adresses"
    )

    commandes = relationship(
        "Commande",
        back_populates="adresse"
    )
