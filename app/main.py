from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import pandas as pd
from src.rag_assistant import suggest_healthy_substitution

app = FastAPI()

df = pd.read_csv("../data/recipes_processed.csv")

class IngredientRequest(BaseModel):
    ingredient: str
    top_n: int = 3

@app.get("/recipes/")
def get_recipes(nutriscore: str = None, diet_type: str = None, difficulty: str = None):
    filtered = df.copy()
    if nutriscore:
        filtered = filtered[filtered["nutriscore"] == nutriscore]
    if diet_type:
        filtered = filtered[filtered["diet_type"] == diet_type]
    if difficulty:
        filtered = filtered[filtered["difficulty"] == difficulty]
    return filtered.head(100).to_dict(orient="records")

@app.post("/suggest_ingredient/")
def suggest_ingredient(req: IngredientRequest):
    return suggest_healthy_substitution(req.ingredient, req.top_n)
