from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import UUID

from app.database import get_db
from app.models.livraison import Livraison
from app.models.commande import Commande
from app.schemas.livraison import LivraisonCreate, LivraisonResponse
from app.routers.utilisateur import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(
    prefix="/livraisons",
    tags=["Livraison"]
)

# =========================
# Créer une livraison
# =========================
@router.post(
    "/{id_commande}",
    response_model=LivraisonResponse,
    status_code=status.HTTP_201_CREATED
)
def creer_livraison(
    id_commande: UUID,
    data: LivraisonCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    # 1️⃣ Vérifier la commande
    commande = db.query(Commande).filter(
        Commande.id_commande == id_commande,
        Commande.id_utilisateur == current_user.id_utilisateur
    ).first()

    if not commande:
        raise HTTPException(
            status_code=404,
            detail="Commande introuvable"
        )

    # 2️⃣ Vérifier paiement
    if commande.statut != "payee":
        raise HTTPException(
            status_code=400,
            detail="Commande non payée"
        )

    # 3️⃣ Vérifier livraison existante
    if commande.livraison:
        raise HTTPException(
            status_code=400,
            detail="Livraison déjà créée"
        )

    # 4️⃣ Créer livraison
    livraison = Livraison(
        id_commande=id_commande,
        type_livraison=data.type_livraison,
        statut="en_preparation",
        date_livraison_prevue=datetime.utcnow() + timedelta(days=2),
        numero_suivi=f"TRACK-{str(id_commande)[:8]}-{int(datetime.utcnow().timestamp())}"
    )

    db.add(livraison)
    db.commit()
    db.refresh(livraison)

    return livraison


# =========================
# Consulter la livraison
# =========================
@router.get(
    "/{id_commande}",
    response_model=LivraisonResponse
)
def get_livraison(
    id_commande: UUID,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    livraison = db.query(Livraison).join(Commande).filter(
        Livraison.id_commande == id_commande,
        Commande.id_utilisateur == current_user.id_utilisateur
    ).first()

    if not livraison:
        raise HTTPException(
            status_code=404,
            detail="Livraison introuvable"
        )

    return livraison
