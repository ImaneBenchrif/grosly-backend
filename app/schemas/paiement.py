from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


# =========================
# Création paiement
# =========================
class PaiementCreate(BaseModel):
    id_commande: UUID
    methode: str  # carte, cash, paypal


# =========================
# Réponse paiement
# =========================
class PaiementResponse(BaseModel):
    id_paiement: UUID
    montant: float
    methode: str
    statut: str

    transaction_id: Optional[str]

    date_paiement: datetime
    date_creation: datetime
    date_modification: datetime

    model_config = ConfigDict(from_attributes=True)
