from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class LignePanierCreate(BaseModel):
    id_produit: int
    quantite: int

class LignePanierResponse(BaseModel):
    id_produit: int
    quantite: int
    prix_unitaire: float

class PanierResponse(BaseModel):
    id_panier: int
    statut: str
    date_creation: datetime
    date_modification: Optional[datetime]
    lignes: List[LignePanierResponse]

    class Config:
        from_attributes = True
