"""
================================================================================
MÓDULO DE UTILIDADES - NutriScript AI
================================================================================

Funciones de apoyo para:
- Limpieza de texto
- Transformaciones de datos
- Validación y manejo de errores
- Cálculos nutricionales

Autor: Senior Data Scientist Team
Versión: 1.0
================================================================================
"""

import re
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple


def clean_text(text: str, lowercase: bool = True, remove_punctuation: bool = True) -> str:
    """
    Limpia y normaliza texto.
    
    Parámetros:
    -----------
    text : str
        Texto a limpiar
    lowercase : bool
        Convertir a minúsculas (default: True)
    remove_punctuation : bool
        Eliminar puntuación (default: True)
    
    Retorna:
    --------
    str : Texto limpio y normalizado
    """
    text = str(text)
    
    if lowercase:
        text = text.lower()
    
    if remove_punctuation:
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    
    # Normalizar espacios
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def parse_nutrition_dict(nutrition_str: str) -> Dict[str, float]:
    """
    Parsea string de nutrición a diccionario.
    
    Parámetros:
    -----------
    nutrition_str : str
        String con lista de valores nutricionales
    
    Retorna:
    --------
    dict : Diccionario con claves ['calories', 'total_fat', 'sat_fat', 'sugar', 'protein', 'sodium', 'fiber']
    """
    try:
        values = eval(nutrition_str)
        return {
            'calories': values[0],
            'total_fat': values[1],
            'sat_fat': values[2],
            'sugar': values[3],
            'protein': values[4],
            'sodium': values[5],
            'fiber': values[6]
        }
    except:
        return {k: np.nan for k in ['calories', 'total_fat', 'sat_fat', 'sugar', 'protein', 'sodium', 'fiber']}


def calculate_macros_percentage(calories: float, protein: float, fat: float, carbs: float) -> Dict[str, float]:
    """
    Calcula porcentaje de macronutrientes.
    
    Parámetros:
    -----------
    calories : float
        Total de calorías
    protein : float
        Gramos de proteína
    fat : float
        Gramos de grasa
    carbs : float
        Gramos de carbohidratos
    
    Retorna:
    --------
    dict : Porcentajes de proteína, grasa, carbohidratos
    """
    if calories == 0:
        return {'protein_pct': 0, 'fat_pct': 0, 'carbs_pct': 0}
    
    protein_cal = protein * 4  # 4 kcal por gramo
    fat_cal = fat * 9          # 9 kcal por gramo
    carbs_cal = carbs * 4      # 4 kcal por gramo
    
    return {
        'protein_pct': (protein_cal / calories) * 100,
        'fat_pct': (fat_cal / calories) * 100,
        'carbs_pct': (carbs_cal / calories) * 100
    }


def get_nutriscore_color(nutriscore: str) -> str:
    """
    Retorna código de color HTML para Nutri-Score.
    
    Parámetros:
    -----------
    nutriscore : str
        Letra de Nutri-Score (A-E)
    
    Retorna:
    --------
    str : Código hex de color
    """
    colors = {
        'A': '#4CAF50',  # Verde
        'B': '#8BC34A',  # Verde claro
        'C': '#FFC107',  # Amarillo
        'D': '#FF9800',  # Naranja
        'E': '#F44336'   # Rojo
    }
    return colors.get(str(nutriscore).upper(), '#CCCCCC')


def get_nutriscore_description(nutriscore: str) -> str:
    """
    Retorna descripción de Nutri-Score.
    
    Parámetros:
    -----------
    nutriscore : str
        Letra de Nutri-Score (A-E)
    
    Retorna:
    --------
    str : Descripción legible
    """
    descriptions = {
        'A': 'Excelente - Muy saludable',
        'B': 'Bueno - Saludable',
        'C': 'Moderado - Aceptable',
        'D': 'Pobre - Poco saludable',
        'E': 'Muy Pobre - Poco recomendado'
    }
    return descriptions.get(str(nutriscore).upper(), 'Desconocido')


def validate_recipe_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valida integridad de datos de recetas.
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con datos de recetas
    
    Retorna:
    --------
    tuple : (is_valid, list_of_issues)
    """
    issues = []
    
    # Columnas requeridas
    required_cols = ['id', 'name', 'steps', 'ingredients', 'nutrition']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        issues.append(f"Columnas faltantes: {missing_cols}")
    
    # Valores nulos
    if df['id'].isna().any():
        issues.append("Existen IDs nulos")
    
    if df['steps'].isna().any():
        issues.append(f"{df['steps'].isna().sum()} recetas sin pasos")
    
    # Duplicados
    if df['id'].duplicated().any():
        issues.append(f"{df['id'].duplicated().sum()} IDs duplicados")
    
    return len(issues) == 0, issues


def filter_recipes_by_nutriscore(df: pd.DataFrame, scores: List[str]) -> pd.DataFrame:
    """
    Filtra recetas por Nutri-Score.
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con recetas
    scores : list
        Lista de scores deseados (ej: ['A', 'B'])
    
    Retorna:
    --------
    pd.DataFrame : Recetas filtradas
    """
    return df[df['nutriscore'].isin(scores)]


def filter_recipes_by_difficulty(df: pd.DataFrame, difficulties: List[str]) -> pd.DataFrame:
    """
    Filtra recetas por dificultad.
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con recetas
    difficulties : list
        Lista de dificultades deseadas (ej: ['Easy', 'Medium'])
    
    Retorna:
    --------
    pd.DataFrame : Recetas filtradas
    """
    return df[df['difficulty'].isin(difficulties)]


def get_nutritional_comparison(recipe1: pd.Series, recipe2: pd.Series) -> Dict:
    """
    Compara información nutricional de dos recetas.
    
    Parámetros:
    -----------
    recipe1 : pd.Series
        Primera receta
    recipe2 : pd.Series
        Segunda receta
    
    Retorna:
    --------
    dict : Comparativa con diferencias
    """
    nutrients = ['calories', 'sugar', 'sat_fat', 'protein', 'sodium']
    
    comparison = {
        'recipe1_name': recipe1.get('name', 'Receta 1'),
        'recipe2_name': recipe2.get('name', 'Receta 2'),
        'differences': {}
    }
    
    for nutrient in nutrients:
        if nutrient in recipe1.index and nutrient in recipe2.index:
            val1 = recipe1[nutrient]
            val2 = recipe2[nutrient]
            diff = val2 - val1
            pct_diff = (diff / val1 * 100) if val1 != 0 else 0
            
            comparison['differences'][nutrient] = {
                'recipe1': val1,
                'recipe2': val2,
                'difference': diff,
                'percent_difference': pct_diff
            }
    
    return comparison
