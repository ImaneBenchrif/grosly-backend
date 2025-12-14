from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from uuid import UUID

from app.database import get_db
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import (
    UtilisateurCreate,
    UtilisateurResponse,
    TokenResponse
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

# ======================================================
# OAuth2 configuration (Swagger Authorize)
# ======================================================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/utilisateurs/login")

router = APIRouter(
    prefix="/utilisateurs",
    tags=["Utilisateurs"]
)

# ======================================================
# REGISTER
# ======================================================
@router.post(
    "/register",
    response_model=UtilisateurResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    utilisateur: UtilisateurCreate,
    db: Session = Depends(get_db)
):
    # Vérifier téléphone
    if db.query(Utilisateur).filter(
        Utilisateur.telephone == utilisateur.telephone
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Téléphone déjà utilisé"
        )

    # Vérifier email
    if db.query(Utilisateur).filter(
        Utilisateur.email == utilisateur.email
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé"
        )

    new_user = Utilisateur(
        full_name=utilisateur.full_name,
        email=utilisateur.email,
        telephone=utilisateur.telephone,
        mot_de_passe=hash_password(utilisateur.mot_de_passe),
        role="user",
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ======================================================
# LOGIN (OAuth2 + JWT)
# ======================================================
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # username = téléphone
    utilisateur = db.query(Utilisateur).filter(
        Utilisateur.telephone == form_data.username
    ).first()

    if not utilisateur or not verify_password(
        form_data.password,
        utilisateur.mot_de_passe
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou mot de passe incorrect"
        )

    access_token = create_access_token(
        data={"sub": str(utilisateur.id_utilisateur)}
    )

    return TokenResponse(
        access_token=access_token
    )


# ======================================================
# GET CURRENT USER (/me)
# ======================================================
@router.get(
    "/me",
    response_model=UtilisateurResponse
)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

    user_id = UUID(payload["sub"])

    utilisateur = db.query(Utilisateur).filter(
        Utilisateur.id_utilisateur == user_id
    ).first()

    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )

    return utilisateur


# ======================================================
# LIST USERS (optionnel / admin)
# ======================================================
@router.get(
    "/",
    response_model=list[UtilisateurResponse]
)
def get_utilisateurs(
    db: Session = Depends(get_db)
):
    return db.query(Utilisateur).all()
