from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID


class CategorieCreate(BaseModel):
    nom: str
    image: Optional[str] = None
    description: Optional[str] = None


class CategorieResponse(BaseModel):
    id_categorie: UUID
    nom: str
    image: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
