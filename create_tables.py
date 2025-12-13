from app.database import engine
from app.models.base import Base

# IMPORTER EXPLICITEMENT TOUS LES MODELS
from app.models.utilisateur import Utilisateur
from app.models.categorie import Categorie
from app.models.produit import Produit

print("Création des tables...")
Base.metadata.create_all(bind=engine)
print("Tables créées avec succès")
