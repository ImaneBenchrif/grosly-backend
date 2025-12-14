from fastapi import FastAPI

from app.routers import (
    utilisateur,
    categorie,
    produit,
    panier,
    commande,
    paiement,
    livraison,
    adresse   # 👈 AJOUT ICI
)

app = FastAPI(title="GroSly API")

# Routers
app.include_router(utilisateur.router)
app.include_router(categorie.router)
app.include_router(produit.router)
app.include_router(panier.router)
app.include_router(commande.router)
app.include_router(paiement.router)
app.include_router(adresse.router)
app.include_router(livraison.router)

@app.get("/")
def root():
    return {"message": "GroSly API is running"}
