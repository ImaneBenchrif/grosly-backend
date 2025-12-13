from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
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

@router.post("/", response_model=CommandeResponse, status_code=status.HTTP_201_CREATED)
def creer_commande(
    data: CommandeCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    # 1️⃣ récupérer le panier actif
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

    # 2️⃣ calculer le total
    montant_total = sum(
        ligne.quantite * ligne.prix_unitaire
        for ligne in lignes_panier
    )

    # 3️⃣ créer la commande
    nouvelle_commande = Commande(
        numero_commande=str(uuid.uuid4()),
        id_utilisateur=current_user.id_utilisateur,
        id_adresse=data.id_adresse,
        montant_total=montant_total,
        notes=data.notes
    )

    db.add(nouvelle_commande)
    db.flush()  # pour avoir id_commande

    # 4️⃣ copier lignes panier → lignes commande
    for ligne in lignes_panier:
        ligne_cmd = LigneCommande(
            id_commande=nouvelle_commande.id_commande,
            id_produit=ligne.id_produit,
            quantite=ligne.quantite,
            prix_unitaire=ligne.prix_unitaire
        )
        db.add(ligne_cmd)

    # 5️⃣ fermer le panier
    panier.statut = "fermé"

    db.commit()
    db.refresh(nouvelle_commande)

    return nouvelle_commande
