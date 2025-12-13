from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LigneCommandeResponse(BaseModel):
    id_produit: int
    quantite: int
    prix_unitaire: float

class CommandeCreate(BaseModel):
    id_adresse: int
    notes: Optional[str] = None

class CommandeResponse(BaseModel):
    id_commande: int
    numero_commande: str
    statut: str
    montant_total: float
    date_commande: datetime
    lignes: List[LigneCommandeResponse]

    class Config:
        from_attributes = True
