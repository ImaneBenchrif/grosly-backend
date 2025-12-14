from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.produit import Produit
from app.models.categorie import Categorie
from app.schemas.produit import ProduitCreate, ProduitResponse

router = APIRouter(
    prefix="/produits",
    tags=["Produits"]
)

# ======================================================
# Créer un produit
# ======================================================
@router.post(
    "/",
    response_model=ProduitResponse,
    status_code=status.HTTP_201_CREATED
)
def creer_produit(
    produit: ProduitCreate,
    db: Session = Depends(get_db)
):
    # Vérifier catégorie
    categorie = db.query(Categorie).filter(
        Categorie.id_categorie == produit.id_categorie
    ).first()

    if not categorie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catégorie introuvable"
        )

    nouveau_produit = Produit(
        nom=produit.nom,
        description=produit.description,
        prix=produit.prix,
        image=produit.image,
        stock=produit.stock,
        origine=produit.origine,
        condition=produit.condition,
        poids=produit.poids,
        promotion=produit.promotion,
        id_categorie=produit.id_categorie
    )

    db.add(nouveau_produit)
    db.commit()
    db.refresh(nouveau_produit)

    return nouveau_produit


# ======================================================
# Lister tous les produits
# ======================================================
@router.get(
    "/",
    response_model=list[ProduitResponse]
)
def lister_produits(db: Session = Depends(get_db)):
    return db.query(Produit).all()


# ======================================================
# Lister produits par catégorie
# ======================================================
@router.get(
    "/categorie/{id_categorie}",
    response_model=list[ProduitResponse]
)
def produits_par_categorie(
    id_categorie: UUID,
    db: Session = Depends(get_db)
):
    return db.query(Produit).filter(
        Produit.id_categorie == id_categorie
    ).all()


# ======================================================
# Récupérer un produit
# ======================================================
@router.get(
    "/{produit_id}",
    response_model=ProduitResponse
)
def get_produit(
    produit_id: UUID,
    db: Session = Depends(get_db)
):
    produit = db.query(Produit).filter(
        Produit.id_produit == produit_id
    ).first()

    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé"
        )

    return produit


# ======================================================
# Modifier un produit
# ======================================================
@router.put(
    "/{produit_id}",
    response_model=ProduitResponse
)
def modifier_produit(
    produit_id: UUID,
    produit: ProduitCreate,
    db: Session = Depends(get_db)
):
    produit_db = db.query(Produit).filter(
        Produit.id_produit == produit_id
    ).first()

    if not produit_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé"
        )

    produit_db.nom = produit.nom
    produit_db.description = produit.description
    produit_db.prix = produit.prix
    produit_db.image = produit.image
    produit_db.stock = produit.stock
    produit_db.origine = produit.origine
    produit_db.condition = produit.condition
    produit_db.poids = produit.poids
    produit_db.promotion = produit.promotion
    produit_db.id_categorie = produit.id_categorie

    db.commit()
    db.refresh(produit_db)

    return produit_db


# ======================================================
# Supprimer un produit
# ======================================================
@router.delete(
    "/{produit_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def supprimer_produit(
    produit_id: UUID,
    db: Session = Depends(get_db)
):
    produit = db.query(Produit).filter(
        Produit.id_produit == produit_id
    ).first()

    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé"
        )

    db.delete(produit)
    db.commit()

    return None
