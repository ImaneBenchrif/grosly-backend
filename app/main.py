from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    utilisateur,
    categorie,
    produit,
    panier,
    commande,
    paiement,
    livraison,
    adresse
)

app = FastAPI(title="GroSly API")

# =========================
# CORS (OBLIGATOIRE POUR FLUTTER / WEB)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ⚠️ OK pour DEV uniquement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTERS
# =========================
app.include_router(utilisateur.router)
app.include_router(categorie.router)
app.include_router(produit.router)
app.include_router(panier.router)
app.include_router(commande.router)
app.include_router(paiement.router)
app.include_router(adresse.router)
app.include_router(livraison.router)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "GroSly API is running"}
