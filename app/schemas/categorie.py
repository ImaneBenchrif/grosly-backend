from pydantic import BaseModel
from typing import Optional

class CategorieCreate(BaseModel):
    nom: str
    image: Optional[str] = None
    description: Optional[str] = None


class CategorieResponse(BaseModel):
    id_categorie: int
    nom: str
    image: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
