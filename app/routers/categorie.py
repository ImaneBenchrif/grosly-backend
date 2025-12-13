from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.categorie import Categorie
from app.schemas.categorie import CategorieCreate, CategorieResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# Créer une catégorie
@router.post("/", response_model=CategorieResponse, status_code=status.HTTP_201_CREATED)
def creer_categorie(categorie: CategorieCreate, db: Session = Depends(get_db)):
    nouvelle_categorie = Categorie(
        nom=categorie.nom,
        image=categorie.image,
        description=categorie.description
    )

    db.add(nouvelle_categorie)
    db.commit()
    db.refresh(nouvelle_categorie)

    return nouvelle_categorie


# Lister les catégories
@router.get("/", response_model=list[CategorieResponse])
def lister_categories(db: Session = Depends(get_db)):
    return db.query(Categorie).all()
