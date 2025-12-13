from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProduitCreate(BaseModel):
    nom: str
    description: str
    prix: float
    image_url: Optional[str] = None
    stock: int
    origine: str
    condition: str
    poids: float
    promotion: float
    id_categorie: int


class ProduitResponse(BaseModel):
    id_produit: int
    nom: str
    description: str
    prix: float
    image: Optional[str]
    stock: int
    origine: str
    condition: str
    poids: float
    promotion: float
    id_categorie: int

    class Config:
        from_attributes = True
