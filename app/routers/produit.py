from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.produit import Produit
from app.schemas.produit import ProduitCreate, ProduitResponse

router = APIRouter(
    prefix="/produits",
    tags=["Produits"]
)

@router.post("/", response_model=ProduitResponse, status_code=status.HTTP_201_CREATED)
def creer_produit(produit: ProduitCreate, db: Session = Depends(get_db)):

    nouveau_produit = Produit(
        nom=produit.nom,
        description=produit.description,
        prix=produit.prix,
        image=produit.image_url,
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


@router.get("/", response_model=list[ProduitResponse])
def lister_produits(db: Session = Depends(get_db)):
    return db.query(Produit).all()

@router.get("/{produit_id}", response_model=ProduitResponse)
def get_produit(produit_id: int, db: Session = Depends(get_db)):
    produit = db.query(Produit).filter(Produit.id_produit == produit_id).first()

    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé"
        )

    return produit

@router.put("/{produit_id}", response_model=ProduitResponse)
def modifier_produit(
    produit_id: int,
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

    # Mise à jour des champs
    produit_db.nom = produit.nom
    produit_db.description = produit.description
    produit_db.prix = produit.prix
    produit_db.image = produit.image_url
    produit_db.stock = produit.stock
    produit_db.origine = produit.origine
    produit_db.condition = produit.condition
    produit_db.poids = produit.poids
    produit_db.promotion = produit.promotion
    produit_db.id_categorie = produit.id_categorie

    db.commit()
    db.refresh(produit_db)

    return produit_db

@router.delete("/{produit_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_produit(
    produit_id: int,
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
