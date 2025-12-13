from pydantic import BaseModel
from datetime import datetime

class PaiementCreate(BaseModel):
    methode: str  # ex: carte, cash, paypal

class PaiementResponse(BaseModel):
    id_paiement: int
    montant: float
    methode: str
    statut: str
    transaction_id: str
    date_paiement: datetime

    class Config:
        from_attributes = True
