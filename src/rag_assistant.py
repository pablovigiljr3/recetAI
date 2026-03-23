"""
Lógica del asistente RAG para NutriScript AI
Sugiere cambios de ingredientes saludables consultando el corpus de recetas.
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Carga corpus de recetas
df = pd.read_csv("../data/recipes_processed.csv")

# Indexación simple por ingredientes
ingredients_corpus = df["ingredients"].astype(str).tolist()
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(ingredients_corpus)

def suggest_healthy_substitution(ingredient, top_n=3):
    """
    Sugiere ingredientes alternativos más saludables basados en similitud semántica y Nutri-Score.
    """
    query_vec = vectorizer.transform([ingredient])
    sims = cosine_similarity(query_vec, X).flatten()
    top_idx = sims.argsort()[-top_n:][::-1]
    suggestions = []
    for idx in top_idx:
        recipe = df.iloc[idx]
        if recipe["nutriscore"] in ["A", "B"]:
            suggestions.append({
                "recipe_id": recipe["id"],
                "ingredient_list": recipe["ingredients"],
                "nutriscore": recipe["nutriscore"]
            })
    return suggestions

if __name__ == "__main__":
    print(suggest_healthy_substitution("butter"))
