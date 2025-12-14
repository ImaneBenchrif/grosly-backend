from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AdresseCreate(BaseModel):
    rue: str
    ville: str
    code_postal: str
    pays: str

class AdresseResponse(BaseModel):
    id_adresse: UUID
    rue: str
    ville: str
    code_postal: str
    pays: str
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True
