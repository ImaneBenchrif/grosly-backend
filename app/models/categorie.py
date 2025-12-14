import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from sqlalchemy.orm import relationship

from .base import Base


class Categorie(Base):
    __tablename__ = "categorie"

    id_categorie = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nom = Column(String(100), nullable=False, unique=True)
    image = Column(String, nullable=True)
    description = Column(Text, nullable=True)

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

    #  Relation inverse avec Produit (OBLIGATOIRE)
    produits = relationship(
        "Produit",
        back_populates="categorie",
        cascade="all, delete-orphan"
    )
