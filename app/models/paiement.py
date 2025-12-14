from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid
from app.models.livraison import Livraison


from .base import Base


class Paiement(Base):
    __tablename__ = "paiement"

    id_paiement = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    montant = Column(
        Float,
        nullable=False
    )

    methode = Column(
        String(50),
        nullable=False
    )  # carte, cash, paypal

    statut = Column(
        String(30),
        default="en_attente",
        nullable=False
    )

    transaction_id = Column(
        String(100),
        nullable=True
    )

    date_paiement = Column(
        DateTime,
        server_default=func.now(),
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

    id_commande = Column(
        UUID(as_uuid=True),
        ForeignKey("commande.id_commande"),
        unique=True,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "montant >= 0",
            name="check_montant_paiement"
        ),
        CheckConstraint(
            "statut IN ('en_attente', 'paye', 'echoue', 'rembourse')",
            name="check_statut_paiement"
        ),
        CheckConstraint(
            "methode IN ('carte', 'cash', 'paypal')",
            name="check_methode_paiement"
        ),
    )

    # Relation
    commande = relationship(
        "Commande",
        back_populates="paiement"
    )
