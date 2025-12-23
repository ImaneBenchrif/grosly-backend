from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def generate_recipe(ingredients: list[str]) -> str:
    # Join ingredients exactly as provided
    ingredients_text = ", ".join(ingredients)

    # Prompt definition
    prompt = f"""
You are a cooking assistant for a Moroccan grocery application.

IMPORTANT RULES (MANDATORY):
- The list of AVAILABLE INGREDIENTS represents what exists in the database.
- AVAILABLE INGREDIENTS MUST ALWAYS be repeated EXACTLY as provided.
- You are allowed to SELECT a subset of ingredients to build ONE coherent dish.
- You MUST NOT say that an available ingredient is missing.
- Missing ingredients must ONLY be complementary items (spices, oil, onion, etc.)
  that are NOT present in the available ingredients list.
- NEVER move an ingredient from available to missing.

Your task:
1) Choose ONE Moroccan dish.
2) Choose ONE main protein if multiple are available (e.g. chicken OR beef).
3) Use vegetables logically if available (e.g. potato).
4) Repeat ALL available ingredients exactly as given.
5) List ONLY complementary missing ingredients.

AVAILABLE INGREDIENTS (DO NOT MODIFY):
{ingredients_text}

Response format (MUST follow exactly):

Bismillah,
Suggested dish: <dish name>
Available ingredients: {ingredients_text}
Missing ingredients: <only complementary ingredients not listed above>
"""

    # Call Groq API
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a strict Moroccan cooking assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    # Return generated content
    return response.choices[0].message.content
