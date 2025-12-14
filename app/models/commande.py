from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text,
    CheckConstraint,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid

from .base import Base


class Commande(Base):
    __tablename__ = "commande"

    id_commande = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    numero_commande = Column(
        String(50),
        unique=True,
        nullable=False
    )

    statut = Column(
        String(30),
        default="en_attente",
        nullable=False
    )

    montant_total = Column(
        Float,
        nullable=False
    )

    notes = Column(
        Text,
        nullable=True
    )

    id_utilisateur = Column(
        UUID(as_uuid=True),
        ForeignKey("utilisateur.id_utilisateur"),
        nullable=False
    )

    id_adresse = Column(
        UUID(as_uuid=True),
        ForeignKey("adresse.id_adresse"),
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
        CheckConstraint(
            "montant_total >= 0",
            name="check_montant_commande_positive"
        ),
        CheckConstraint(
            "statut IN ('en_attente', 'payee', 'annulee', 'expediee', 'livree')",
            name="check_statut_commande"
        ),
        Index("idx_commande_utilisateur", "id_utilisateur"),
        Index("idx_commande_date", "date_creation"),
    )

    # Relations
    utilisateur = relationship(
        "Utilisateur",
        back_populates="commandes"
    )

    lignes = relationship(
        "LigneCommande",
        back_populates="commande",
        cascade="all, delete-orphan"
    )

    adresse = relationship(
        "Adresse",
        back_populates="commandes"
    )

    paiement = relationship(
        "Paiement",
        back_populates="commande",
        uselist=False
    )

    livraison = relationship(
        "Livraison",
        back_populates="commande",
        uselist=False
    )
