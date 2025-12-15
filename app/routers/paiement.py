from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta

from app.database import get_db
from app.models.paiement import Paiement
from app.models.commande import Commande
from app.models.livraison import Livraison
from app.schemas.paiement import PaiementCreate, PaiementResponse
from app.routers.utilisateur import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(
    prefix="/paiements",
    tags=["Paiement"]
)

@router.post(
    "/",
    response_model=PaiementResponse,
    status_code=status.HTTP_201_CREATED
)
def payer_commande(
    data: PaiementCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    # 1️⃣ Vérifier commande
    commande = db.query(Commande).filter(
        Commande.id_commande == data.id_commande,
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

    # 2️⃣ Créer paiement
    paiement = Paiement(
        montant=commande.montant_total,
        methode=data.methode,
        statut="paye",
        transaction_id=str(uuid.uuid4()),
        id_commande=commande.id_commande
    )

    # 3️⃣ Mettre à jour commande
    commande.statut = "payee"

    # 4️⃣ CRÉER LIVRAISON SI ELLE N’EXISTE PAS
    livraison_existante = db.query(Livraison).filter(
        Livraison.id_commande == commande.id_commande
    ).first()

    if not livraison_existante:
        livraison = Livraison(
            id_commande=commande.id_commande,
            type_livraison="standard",
            statut="en_preparation",
            numero_suivi=f"TRACK-{uuid.uuid4().hex[:8].upper()}",
            date_livraison_prevue=datetime.utcnow() + timedelta(days=3),
            duree_estimee="3 jours"
        )
        db.add(livraison)

    db.add(paiement)
    db.commit()
    db.refresh(paiement)

    return paiement
