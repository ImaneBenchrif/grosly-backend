from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.paiement import Paiement
from app.models.commande import Commande
from app.schemas.paiement import PaiementCreate, PaiementResponse
from app.routers.utilisateur import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(
    prefix="/paiements",
    tags=["Paiement"]
)


@router.post("/", response_model=PaiementResponse, status_code=status.HTTP_201_CREATED)
def payer_commande(
    paiement: PaiementCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    commande = db.query(Commande).filter(
        Commande.id_commande == paiement.id_commande,
        Commande.id_utilisateur == current_user.id_utilisateur
    ).first()

    if not commande:
        raise HTTPException(
            status_code=404,
            detail="Commande introuvable"
        )

    if commande.statut != "en_attente":
        raise HTTPException(
            status_code=400,
            detail="Commande déjà payée ou invalide"
        )

    # Créer paiement simulé
    nouveau_paiement = Paiement(
        montant=commande.montant_total,
        methode=paiement.methode,
        statut="payé",
        transaction_id=str(uuid.uuid4()),
        id_commande=commande.id_commande
    )

    # Mettre à jour commande
    commande.statut = "payee"

    db.add(nouveau_paiement)
    db.commit()
    db.refresh(nouveau_paiement)

    return nouveau_paiement
