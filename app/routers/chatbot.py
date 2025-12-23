from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.produit import Produit
from app.utils.groq_client import generate_recipe

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"]
)

@router.post("/recipe")
def recipe_chatbot(db: Session = Depends(get_db)):
    produits = db.query(Produit).filter(
        Produit.stock > 0
    ).all()

    ingredients = [p.nom for p in produits if p.nom]

    if not ingredients:
        return {"message": "No ingredients found in database"}
    response = generate_recipe(ingredients)

    return {
        "ingredients": ingredients,
        "chatbot_response": response
    }


