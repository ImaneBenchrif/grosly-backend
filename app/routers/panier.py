from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.panier import Panier
from app.models.ligne_panier import LignePanier
from app.models.produit import Produit
from app.schemas.panier import PanierResponse, LignePanierCreate
from app.routers.utilisateur import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(
    prefix="/panier",
    tags=["Panier"]
)

# ======================================================
# Utilitaire : récupérer ou créer panier actif
# ======================================================
def get_or_create_panier(
    db: Session,
    utilisateur_id: UUID
) -> Panier:
    panier = db.query(Panier).filter(
        Panier.id_utilisateur == utilisateur_id,
        Panier.statut == "actif"
    ).first()

    if not panier:
        panier = Panier(id_utilisateur=utilisateur_id)
        db.add(panier)
        db.commit()
        db.refresh(panier)

    return panier


# ======================================================
# Voir le panier
# ======================================================
@router.get("/", response_model=PanierResponse)
def get_panier(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    return get_or_create_panier(db, current_user.id_utilisateur)


# ======================================================
# Ajouter produit au panier
# ======================================================
@router.post("/ajouter", response_model=PanierResponse)
def ajouter_au_panier(
    ligne: LignePanierCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    panier = get_or_create_panier(db, current_user.id_utilisateur)

    produit = db.query(Produit).filter(
        Produit.id_produit == ligne.id_produit
    ).first()

    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable"
        )

    ligne_existante = db.query(LignePanier).filter(
        LignePanier.id_panier == panier.id_panier,
        LignePanier.id_produit == ligne.id_produit
    ).first()

    if ligne_existante:
        ligne_existante.quantite += ligne.quantite
    else:
        nouvelle_ligne = LignePanier(
            id_panier=panier.id_panier,
            id_produit=ligne.id_produit,
            quantite=ligne.quantite,
            prix_unitaire=produit.prix
        )
        db.add(nouvelle_ligne)

    db.commit()
    db.refresh(panier)

    return panier


# ======================================================
# Modifier quantité
# ======================================================
@router.put("/modifier", response_model=PanierResponse)
def modifier_quantite(
    ligne: LignePanierCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    panier = get_or_create_panier(db, current_user.id_utilisateur)

    ligne_panier = db.query(LignePanier).filter(
        LignePanier.id_panier == panier.id_panier,
        LignePanier.id_produit == ligne.id_produit
    ).first()

    if not ligne_panier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non présent dans le panier"
        )

    ligne_panier.quantite = ligne.quantite

    db.commit()
    db.refresh(panier)

    return panier


# ======================================================
# Supprimer un produit du panier
# ======================================================
@router.delete(
    "/supprimer/{id_produit}",
    response_model=PanierResponse
)
def supprimer_produit(
    id_produit: UUID,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    panier = get_or_create_panier(db, current_user.id_utilisateur)

    ligne = db.query(LignePanier).filter(
        LignePanier.id_panier == panier.id_panier,
        LignePanier.id_produit == id_produit
    ).first()

    if not ligne:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non présent dans le panier"
        )

    db.delete(ligne)
    db.commit()
    db.refresh(panier)

    return panier
