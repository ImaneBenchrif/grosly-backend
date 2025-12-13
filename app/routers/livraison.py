from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

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
@router.post("/{id_commande}", response_model=LivraisonResponse)
def creer_livraison(
    id_commande: int,
    data: LivraisonCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    commande = db.query(Commande).filter(
        Commande.id_commande == id_commande,
        Commande.id_utilisateur == current_user.id_utilisateur
    ).first()

    if not commande:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    if commande.livraison:
        raise HTTPException(status_code=400, detail="Livraison déjà créée")

    livraison = Livraison(
        id_commande=id_commande,
        type_livraison=data.type_livraison,
        statut="en_preparation",
        date_livraison_prevue=datetime.utcnow() + timedelta(days=2),
        numero_suivi=f"TRACK-{id_commande}-{int(datetime.utcnow().timestamp())}"
    )

    db.add(livraison)
    db.commit()
    db.refresh(livraison)

    return livraison
@router.get("/{id_commande}", response_model=LivraisonResponse)
def get_livraison(
    id_commande: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    livraison = db.query(Livraison).join(Commande).filter(
        Livraison.id_commande == id_commande,
        Commande.id_utilisateur == current_user.id_utilisateur
    ).first()

    if not livraison:
        raise HTTPException(status_code=404, detail="Livraison introuvable")

    return livraison
