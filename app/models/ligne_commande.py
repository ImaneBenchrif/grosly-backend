from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .base import Base


class LigneCommande(Base):
    __tablename__ = "ligne_commande"

    id_commande = Column(
        UUID(as_uuid=True),
        ForeignKey("commande.id_commande"),
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
        CheckConstraint(
            "quantite > 0",
            name="check_quantite_ligne_commande"
        ),
        CheckConstraint(
            "prix_unitaire >= 0",
            name="check_prix_unitaire_ligne_commande"
        ),
    )

    # Relations
    commande = relationship(
        "Commande",
        back_populates="lignes"
    )

    produit = relationship(
        "Produit"
    )
