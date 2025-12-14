from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class ProduitCreate(BaseModel):
    nom: str
    prix: float

    description: Optional[str] = None
    image: Optional[str] = None

    stock: Optional[int] = 0

    origine: Optional[str] = None
    condition: Optional[str] = None
    poids: Optional[float] = None
    promotion: Optional[float] = None

    id_categorie: UUID


class ProduitResponse(BaseModel):
    id_produit: UUID
    nom: str
    prix: float

    description: Optional[str]
    image: Optional[str]

    stock: int
    origine: Optional[str]
    condition: Optional[str]
    poids: Optional[float]
    promotion: Optional[float]

    id_categorie: UUID

    date_creation: datetime
    date_modification: datetime

    model_config = ConfigDict(from_attributes=True)
