from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid

from .base import Base


class Livraison(Base):
    __tablename__ = "livraison"

    id_livraison = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    type_livraison = Column(
        String(50),
        nullable=False
    )  # standard, express

    statut = Column(
        String(30),
        default="en_preparation",
        nullable=False
    )

    numero_suivi = Column(
        String(100),
        nullable=True
    )

    duree_estimee = Column(
        String(50),
        nullable=True
    )

    date_livraison_prevue = Column(
        DateTime,
        nullable=True
    )

    date_livraison_reelle = Column(
        DateTime,
        nullable=True
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

    id_commande = Column(
        UUID(as_uuid=True),
        ForeignKey("commande.id_commande"),
        unique=True,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "type_livraison IN ('standard', 'express')",
            name="check_type_livraison"
        ),
        CheckConstraint(
            "statut IN ('en_preparation', 'expediee', 'en_cours', 'livree', 'annulee')",
            name="check_statut_livraison"
        ),
    )

    # Relation
    commande = relationship(
        "Commande",
        back_populates="livraison"
    )
