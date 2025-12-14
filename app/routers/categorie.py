from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.categorie import Categorie
from app.schemas.categorie import CategorieCreate, CategorieResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# ======================================================
# Créer une catégorie
# ======================================================
@router.post(
    "/",
    response_model=CategorieResponse,
    status_code=status.HTTP_201_CREATED
)
def creer_categorie(
    categorie: CategorieCreate,
    db: Session = Depends(get_db)
):
    # Vérifier doublon
    if db.query(Categorie).filter(
        Categorie.nom == categorie.nom
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cette catégorie existe déjà"
        )

    nouvelle_categorie = Categorie(
        nom=categorie.nom,
        image=categorie.image,
        description=categorie.description
    )

    db.add(nouvelle_categorie)
    db.commit()
    db.refresh(nouvelle_categorie)

    return nouvelle_categorie


# ======================================================
# Lister toutes les catégories
# ======================================================
@router.get(
    "/",
    response_model=list[CategorieResponse]
)
def lister_categories(db: Session = Depends(get_db)):
    return db.query(Categorie).all()


# ======================================================
# Récupérer une catégorie par ID
# ======================================================
@router.get(
    "/{id_categorie}",
    response_model=CategorieResponse
)
def get_categorie(
    id_categorie: UUID,
    db: Session = Depends(get_db)
):
    categorie = db.query(Categorie).filter(
        Categorie.id_categorie == id_categorie
    ).first()

    if not categorie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catégorie non trouvée"
        )

    return categorie
