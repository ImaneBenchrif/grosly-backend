from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


# =========================
# Création livraison
# =========================
class LivraisonCreate(BaseModel):
    type_livraison: str = "standard"


# =========================
# Réponse livraison
# =========================
class LivraisonResponse(BaseModel):
    id_livraison: UUID

    type_livraison: str
    statut: str

    numero_suivi: Optional[str]
    duree_estimee: Optional[str]

    date_livraison_prevue: Optional[datetime]
    date_livraison_reelle: Optional[datetime]

    date_creation: datetime
    date_modification: datetime

    model_config = ConfigDict(from_attributes=True)
