from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime


# =========================
# Lignes de commande
# =========================
class LigneCommandeResponse(BaseModel):
    id_produit: UUID
    quantite: int
    prix_unitaire: float

    date_creation: datetime
    date_modification: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# Création commande
# =========================
class CommandeCreate(BaseModel):
    id_adresse: UUID
    notes: Optional[str] = None


# =========================
# Réponse commande
# =========================
class CommandeResponse(BaseModel):
    id_commande: UUID
    numero_commande: str
    statut: str
    montant_total: float
    notes: Optional[str]

    date_creation: datetime
    date_modification: datetime

    lignes: List[LigneCommandeResponse]

    model_config = ConfigDict(from_attributes=True)
