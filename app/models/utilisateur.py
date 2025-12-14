from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid

from .base import Base


class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telephone = Column(String(30), unique=True, nullable=False, index=True)

    mot_de_passe = Column(String(255), nullable=False)

    role = Column(String(50), default="user", nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

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
    panier = relationship(
        "Panier",
        back_populates="utilisateur",
        uselist=False,
        cascade="all, delete-orphan"
    )

    commandes = relationship(
        "Commande",
        back_populates="utilisateur"
    )

    adresses = relationship(
        "Adresse",
        back_populates="utilisateur"
    )
