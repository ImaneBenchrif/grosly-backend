from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import uuid

from app.database import get_db
from app.models.commande import Commande
from app.models.ligne_commande import LigneCommande
from app.models.panier import Panier
from app.models.ligne_panier import LignePanier
from app.models.utilisateur import Utilisateur
from app.schemas.commande import CommandeResponse, CommandeCreate
from app.routers.utilisateur import get_current_user

router = APIRouter(
    prefix="/commandes",
    tags=["Commandes"]
)

# ======================================================
# POST /commandes → créer une commande depuis le panier
# ======================================================
@router.post(
    "/",
    response_model=CommandeResponse,
    status_code=status.HTTP_201_CREATED
)
def creer_commande(
    data: CommandeCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    # 1️⃣ Panier actif
    panier = db.query(Panier).filter(
        Panier.id_utilisateur == current_user.id_utilisateur,
        Panier.statut == "actif"
    ).first()

    if not panier:
        raise HTTPException(
            status_code=400,
            detail="Aucun panier actif"
        )

    lignes_panier = db.query(LignePanier).filter(
        LignePanier.id_panier == panier.id_panier
    ).all()

    if not lignes_panier:
        raise HTTPException(
            status_code=400,
            detail="Panier vide"
        )

    # 2️⃣ Calcul total
    montant_total = sum(
        lp.quantite * lp.prix_unitaire
        for lp in lignes_panier
    )

    # 3️⃣ Création commande
    commande = Commande(
        numero_commande=f"CMD-{uuid.uuid4().hex[:10].upper()}",
        id_utilisateur=current_user.id_utilisateur,
        id_adresse=data.id_adresse,
        montant_total=montant_total,
        notes=data.notes
    )

    db.add(commande)
    db.flush()  # récupérer id_commande

    # 4️⃣ Copier lignes panier → lignes commande
    for lp in lignes_panier:
        db.add(
            LigneCommande(
                id_commande=commande.id_commande,
                id_produit=lp.id_produit,
                quantite=lp.quantite,
                prix_unitaire=lp.prix_unitaire
            )
        )

    # 5️⃣ Fermer panier
    panier.statut = "ferme"

    db.commit()
    db.refresh(commande)

    return commande


# ======================================================
# GET /commandes → lister les commandes de l'utilisateur
# ======================================================
@router.get(
    "/",
    response_model=list[CommandeResponse]
)
def lister_commandes(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    commandes = db.query(Commande).filter(
        Commande.id_utilisateur == current_user.id_utilisateur
    ).order_by(Commande.date_creation.desc()).all()

    return commandes


# ======================================================
# GET /commandes/{id_commande} → détail commande
# ======================================================
@router.get(
    "/{id_commande}",
    response_model=CommandeResponse
)
def get_commande(
    id_commande: UUID,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    commande = db.query(Commande).filter(
        Commande.id_commande == id_commande,
        Commande.id_utilisateur == current_user.id_utilisateur
    ).first()

    if not commande:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commande introuvable"
        )

    return commande
