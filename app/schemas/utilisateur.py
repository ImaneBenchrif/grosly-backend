from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UtilisateurCreate(BaseModel):
    full_name: str
    email: EmailStr
    telephone: str
    mot_de_passe: str

class UtilisateurLogin(BaseModel):
    telephone: str
    mot_de_passe: str

class UtilisateurResponse(BaseModel):
    id_utilisateur: int
    full_name: str
    email: EmailStr
    telephone: str
    role: str
    is_verified: bool
    date_creation: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
