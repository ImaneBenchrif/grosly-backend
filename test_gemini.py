from google import genai
import os

# Initialisation du client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def list_available_models():
    """Liste tous les modèles disponibles et leurs méthodes supportées"""
    try:
        models = client.models.list()
        print("Modèles disponibles :\n")
        for model in models:
            print(f"- {model.name}")
            print(f"  Méthodes supportées : {model.supported_generation_methods}\n")
    except Exception as e:
        print(f"Erreur lors de la récupération des modèles : {e}")

def test_first_compatible_model():
    """Teste le premier modèle compatible avec generateContent"""
    models = client.models.list()
    for model in models:
        if "generateContent" in model.supported_generation_methods:
            print(f"\nTest du modèle : {model.name}")
            response = client.models.generate_content(
                model=model.name,
                contents="Say hello"
            )
            if response.candidates:
                print("Réponse :", response.candidates[0].content.parts[0].text)
            else:
                print("Aucune réponse")
            return

    print("Aucun modèle compatible avec generateContent trouvé.")

# 🔍 1️⃣ Lister les modèles
list_available_models()

# 🧪 2️⃣ Tester automatiquement un modèle valide
test_first_compatible_model()
