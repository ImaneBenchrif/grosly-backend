from app.schemas.paiement import PaiementCreate

p = PaiementCreate(
    methode="carte",
    montant=120.5
)

print(p)
