from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LivraisonCreate(BaseModel):
    type_livraison: str = "standard"


class LivraisonResponse(BaseModel):
    id_livraison: int
    type_livraison: str
    statut: str
    date_livraison_prevue: Optional[datetime]
    date_livraison_reelle: Optional[datetime]
    numero_suivi: Optional[str]

    class Config:
        from_attributes = True
