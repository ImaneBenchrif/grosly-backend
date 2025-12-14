from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from uuid import UUID


# -------- Ligne Panier --------

class LignePanierCreate(BaseModel):
    id_produit: UUID
    quantite: int


class LignePanierResponse(BaseModel):
    id_produit: UUID
    quantite: int
    prix_unitaire: float

    date_creation: datetime
    date_modification: datetime

    model_config = ConfigDict(from_attributes=True)


# -------- Panier --------

class PanierResponse(BaseModel):
    id_panier: UUID
    statut: str

    date_creation: datetime
    date_modification: datetime

    lignes: List[LignePanierResponse]

    model_config = ConfigDict(from_attributes=True)
