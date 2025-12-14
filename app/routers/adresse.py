from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.adresse import Adresse
from app.schemas.adresse import AdresseCreate, AdresseResponse
from app.routers.utilisateur import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(
    prefix="/adresses",
    tags=["Adresses"]
)

# ======================================================
# CRÉER UNE ADRESSE
# ======================================================
@router.post(
    "/",
    response_model=AdresseResponse,
    status_code=status.HTTP_201_CREATED
)
def creer_adresse(
    adresse: AdresseCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    nouvelle_adresse = Adresse(
        rue=adresse.rue,
        ville=adresse.ville,
        code_postal=adresse.code_postal,
        pays=adresse.pays,
        id_utilisateur=current_user.id_utilisateur
    )

    db.add(nouvelle_adresse)
    db.commit()
    db.refresh(nouvelle_adresse)

    return nouvelle_adresse


# ======================================================
# LISTE DES ADRESSES DE L’UTILISATEUR
# ======================================================
@router.get("/", response_model=list[AdresseResponse])
def lister_adresses(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    return db.query(Adresse).filter(
        Adresse.id_utilisateur == current_user.id_utilisateur
    ).all()
