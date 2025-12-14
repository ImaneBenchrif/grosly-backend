from app.database import engine
from app.models.base import Base

# IMPORTER TOUS LES MODELS (OBLIGATOIRE)
from app.models.utilisateur import Utilisateur
from app.models.categorie import Categorie
from app.models.produit import Produit
from app.models.panier import Panier
from app.models.ligne_panier import LignePanier
from app.models.commande import Commande
from app.models.ligne_commande import LigneCommande
from app.models.paiement import Paiement
from app.models.livraison import Livraison
from app.models.adresse import Adresse

print("Création des tables...")
Base.metadata.create_all(bind=engine)
print("Tables créées avec succès")
