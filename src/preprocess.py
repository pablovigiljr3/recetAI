"""
================================================================================
MÓDULO DE PREPROCESAMIENTO - NutriScript AI
================================================================================

Objetivo:
---------
Transformar datos crudos de recetas (RAW_recipes.csv) en información estructurada
y semánticamente procesada para análisis NLP avanzado.

Características Principales:
---------------------------
1. CARGA EFICIENTE: Manejo de 30,000 registros sin overhead de memoria
2. PROCESAMIENTO MASIVO: spaCy nlp.pipe() con paralelización (n_process=-1)
3. EXTRACCIÓN DE FEATURES LINGÜÍSTICAS: Lematización, POS tagging, verbos de acción
4. INGENIERÍA DE ETIQUETAS: Nutri-Score (A-E), Tipo de Dieta, Nivel de Dificultad

Optimizaciones Técnicas:
------------------------
- nlp.pipe() procesa lotes en paralelo (~3000-5000 docs/sec)
- Desactivar ["parser", "ner"] acelera 3-5x (solo necesitamos tokenización)
- n_process=-1 usa todos los CPU cores disponibles

Estructura de Salida:
---------------------
df[
    'id', 'name', 'minutes', 'n_steps',
    'lemmas',           # Texto lematizado (para TF-IDF)
    'action_verbs',     # Verbos de acción extraídos
    'nutriscore',       # A-E (target principal)
    'diet_type',        # Vegan, Vegetarian, Keto, Other
    'difficulty'        # Easy, Medium, Hard
]

Autor: Senior Data Scientist Team
Versión: 1.0
================================================================================
"""

import pandas as pd
import numpy as np
import spacy
from tqdm import tqdm
import ast
import warnings
warnings.filterwarnings('ignore')

tqdm.pandas()


class NutriscriptPreprocessor:
    """Clase principal para preprocesamiento de recetas en NutriScript AI"""
    
    def __init__(self, nlp_model='en_core_web_sm'):
        """
        Inicializa el preprocesador con modelo spaCy.
        
        Parámetros:
        -----------
        nlp_model : str
            Nombre del modelo spaCy a usar (default: 'en_core_web_sm')
        """
        try:
            self.nlp = spacy.load(nlp_model, disable=["parser", "ner"])
            print(f"✓ Modelo spaCy '{nlp_model}' cargado correctamente")
        except OSError:
            print(f"✗ Modelo '{nlp_model}' no encontrado. Descargando...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "spacy", "download", nlp_model])
            self.nlp = spacy.load(nlp_model, disable=["parser", "ner"])
            print(f"✓ Modelo descargado e instalado")
    
    @staticmethod
    def load_data(path: str, sample_size: int = 30000, random_state: int = 42) -> pd.DataFrame:
        """
        Carga dataset de forma eficiente con opción de muestreo.
        
        Parámetros:
        -----------
        path : str
            Ruta al archivo CSV
        sample_size : int
            Número de registros a procesar (default: 30000)
        random_state : int
            Seed para reproducibilidad
        
        Retorna:
        --------
        pd.DataFrame : Dataset cargado (sin recortes si len < sample_size)
        """
        df = pd.read_csv(path)
        print(f"📊 Dataset original: {len(df):,} registros")
        
        if len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=random_state)
            print(f"📊 Muestra tomada: {len(df):,} registros")
        
        return df.reset_index(drop=True)
    
    def spacy_process_texts(self, texts: list, batch_size: int = 1000) -> list:
        """
        Procesa textos masivamente con spaCy usando nlp.pipe()
        
        Ventajas de nlp.pipe():
        - Procesa lotes en paralelo
        - n_process=-1 utiliza TODOS los cores
        - ~3000-5000 docs/segundo (vs 100-200 con documento individual)
        
        Parámetros:
        -----------
        texts : list
            Lista de textos a procesar
        batch_size : int
            Tamaño del lote para procesamiento (default: 1000)
        
        Retorna:
        --------
        list : Lista de objetos Doc de spaCy procesados
        """
        print(f"\\n⚙️ Procesando {len(texts):,} textos con spaCy...\"\"\"
        print(f\"  - Configuración: n_process=-1 (todos los cores)\")\n        print(f\"  - Batch size: {batch_size}\")\n        print(f\"  - Componentes desactivados: parser, ner\")\n        
        docs = list(self.nlp.pipe(texts, batch_size=batch_size, n_process=-1))
        return docs
    
    @staticmethod
    def extract_lemmas_pos(docs: list) -> tuple:
        \"\"\"
        Extrae lemas y POS tags de documentos procesados con spaCy.
        
        Lematización: Normaliza variaciones morfológicas
        - \"cooking\", \"cooks\", \"cooked\" → \"cook\"\n        - \"baking\", \"bakes\" → \"bake\"\n        \n        POS Tagging: Identifica parte del discurso\n        - VERB: cooking, mixing, baking → acciones culinarias\n        \n        Parámetros:\n        -----------\n        docs : list\n            Lista de objetos Doc de spaCy\n        \n        Retorna:\n        --------\n        tuple : (lemmas, action_verbs)\n            - lemmas : str con palabras lematizadas\n            - action_verbs : str con solo verbos (POS == VERB)\n        \"\"\"\n        lemmatized = []\n        action_verbs = []\n        \n        for doc in docs:\n            # Lemas\n            lemas = \" \".join([token.lemma_ for token in doc])\n            lemmatized.append(lemas)\n            \n            # Verbos de acción\n            verbos = \" \".join([token.lemma_ for token in doc if token.pos_ == \"VERB\"])\n            action_verbs.append(verbos)\n        \n        return lemmatized, action_verbs\n    \n    @staticmethod\n    def extract_n_steps(steps_str: str) -> int:\n        \"\"\"\n        Extrae número de pasos de instrucciones (formato lista en string).\n        \"\"\"\n        try:\n            steps_list = ast.literal_eval(steps_str)\n            return len(steps_list)\n        except:\n            return np.nan\n    \n    @staticmethod\n    def compute_nutriscore(sugar: float, sat_fat: float) -> str:\n        \"\"\"\n        Calcula Nutri-Score basándose en azúcar y grasas saturadas.\n        \n        Umbral de Nutrición (basado en análisis EDA):\n        - A (Excelente):     azúcar < 5g AND grasas < 2g\n        - B (Bueno):         azúcar < 10g AND grasas < 4g\n        - C (Moderado):      azúcar < 15g AND grasas < 6g\n        - D (Pobre):         azúcar < 20g AND grasas < 8g\n        - E (Muy Pobre):     resto\n        \n        Parámetros:\n        -----------\n        sugar : float\n            Gramos de azúcar\n        sat_fat : float\n            Gramos de grasas saturadas\n        \n        Retorna:\n        --------\n        str : Letra de Nutri-Score (A, B, C, D, E)\n        \"\"\"\n        try:\n            sugar = float(sugar)\n            sat_fat = float(sat_fat)\n            \n            if sugar < 5 and sat_fat < 2:\n                return 'A'\n            elif sugar < 10 and sat_fat < 4:\n                return 'B'\n            elif sugar < 15 and sat_fat < 6:\n                return 'C'\n            elif sugar < 20 and sat_fat < 8:\n                return 'D'\n            else:\n                return 'E'\n        except:\n            return np.nan\n    \n    @staticmethod\n    def classify_diet(tags: str) -> str:\n        \"\"\"\n        Clasifica tipo de dieta basándose en tags.\n        \n        Jerarquía de clasificación:\n        1. Vegan (sin productos animales)\n        2. Vegetarian (excepto carne)\n        3. Gluten-Free (sin gluten)\n        4. Keto (bajos carbohidratos)\n        5. Paleo (alimentos primitivos)\n        6. Other (sin restricción específica)\n        \n        Parámetros:\n        -----------\n        tags : str\n            String con tags de la receta\n        \n        Retorna:\n        --------\n        str : Categoría de dieta\n        \"\"\"\n        tags = str(tags).lower()\n        \n        if \"vegan\" in tags:\n            return \"Vegan\"\n        elif \"vegetarian\" in tags:\n            return \"Vegetarian\"\n        elif \"gluten\" in tags and \"free\" in tags:\n            return \"Gluten-Free\"\n        elif \"keto\" in tags:\n            return \"Keto\"\n        elif \"paleo\" in tags:\n            return \"Paleo\"\n        else:\n            return \"Other\"\n    \n    @staticmethod\n    def classify_difficulty(n_steps: float, minutes: float) -> str:\n        \"\"\"\n        Clasifica dificultad basándose en número de pasos y tiempo.\n        \n        Umbrales empirícos (basado en análisis de correlación):\n        - Easy:   ≤ 5 pasos AND ≤ 30 minutos\n        - Medium: ≤ 10 pasos AND ≤ 60 minutos\n        - Hard:   > 10 pasos OR > 60 minutos\n        \n        Parámetros:\n        -----------\n        n_steps : float\n            Número de pasos en la receta\n        minutes : float\n            Tiempo total en minutos\n        \n        Retorna:\n        --------\n        str : Nivel de dificultad (Easy, Medium, Hard)\n        \"\"\"\n        try:\n            n_steps = float(n_steps)\n            minutes = float(minutes)\n            \n            if n_steps <= 5 and minutes <= 30:\n                return \"Easy\"\n            elif n_steps <= 10 and minutes <= 60:\n                return \"Medium\"\n            else:\n                return \"Hard\"\n        except:\n            return np.nan\n    \n    def preprocess_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:\n        \"\"\"\n        Pipeline completo de preprocesamiento.\n        \n        Pasos:\n        1. Procesar textos con spaCy\n        2. Extraer lemas y POS tags\n        3. Extraer información nutricional\n        4. Crear targets (Nutri-Score, Dificultad, Tipo Dieta)\n        5. Limpiar y validar\n        \n        Parámetros:\n        -----------\n        df : pd.DataFrame\n            DataFrame con datos crudos\n        \n        Retorna:\n        --------\n        pd.DataFrame : Dataset preprocesado y enriquecido\n        \"\"\"\n        print(f\"\\n📝 INICIANDO PIPELINE DE PREPROCESAMIENTO\")\n        print(f\"=\"*80)\n        \n        # 1. Procesar steps con spaCy\n        print(f\"\\n1️⃣ Procesamiento masivo con spaCy...\")\n        docs = self.spacy_process_texts(df[\"steps\"].astype(str))\n        df[\"lemmas\"], df[\"action_verbs\"] = self.extract_lemmas_pos(docs)\n        print(f\"✓ Lematización y POS tagging completados\")\n        \n        # 2. Extraer número de pasos\n        print(f\"\\n2️⃣ Extrayendo features de dificultad...\")\n        df['n_steps'] = df['steps'].progress_apply(self.extract_n_steps)\n        df['minutes'] = pd.to_numeric(df['minutes'], errors='coerce')\n        print(f\"✓ Features de dificultad extraídos\")\n        \n        # 3. Extraer nutrientes\n        print(f\"\\n3️⃣ Extrayendo información nutricional...\")\n        def parse_nutrition(nutrition_str):\n            try:\n                return ast.literal_eval(nutrition_str)\n            except:\n                return None\n        \n        df['nutrition_list'] = df['nutrition'].progress_apply(parse_nutrition)\n        df['calories'] = df['nutrition_list'].apply(lambda x: x[0] if x else np.nan)\n        df['total_fat'] = df['nutrition_list'].apply(lambda x: x[1] if x else np.nan)\n        df['sat_fat'] = df['nutrition_list'].apply(lambda x: x[2] if x else np.nan)\n        df['sugar'] = df['nutrition_list'].apply(lambda x: x[3] if x else np.nan)\n        df['protein'] = df['nutrition_list'].apply(lambda x: x[4] if x else np.nan)\n        df['sodium'] = df['nutrition_list'].apply(lambda x: x[5] if x else np.nan)\n        print(f\"✓ Nutrientes extraídos\")\n        \n        # 4. Crear targets\n        print(f\"\\n4️⃣ Creando targets de clasificación...\")\n        df['nutriscore'] = df.progress_apply(\n            lambda row: self.compute_nutriscore(row['sugar'], row['sat_fat']), \n            axis=1\n        )\n        df['diet_type'] = df['tags'].progress_apply(self.classify_diet)\n        df['difficulty'] = df.progress_apply(\n            lambda row: self.classify_difficulty(row['n_steps'], row['minutes']),\n            axis=1\n        )\n        print(f\"✓ Targets creados\")\n        \n        # 5. Limpiar\n        print(f\"\\n5️⃣ Validación y limpieza...\")\n        print(f\"  - Nulos en lemmas: {df['lemmas'].isna().sum()}\")\n        print(f\"  - Nulos en nutriscore: {df['nutriscore'].isna().sum()}\")\n        print(f\"  - Nulos en dificultad: {df['difficulty'].isna().sum()}\")\n        \n        print(f\"\\n✅ PIPELINE COMPLETADO\")\n        print(f\"=\"*80)\n        print(f\"\\nDataset final: {len(df):,} registros × {len(df.columns)} columnas\")\n        \n        return df


if __name__ == \"__main__\":\n    # Ejecutar pipeline completo\n    preprocessor = NutriscriptPreprocessor()\n    df = preprocessor.load_data(\"../data/RAW_recipes.csv\", sample_size=30000)\n    df = preprocessor.preprocess_pipeline(df)\n    \n    # Guardar\n    output_cols = [\n        'id', 'name', 'minutes', 'n_steps', 'calories', 'sugar', 'sat_fat', 'protein',\n        'lemmas', 'action_verbs', 'nutriscore', 'difficulty', 'diet_type', \n        'ingredients', 'steps', 'tags'\n    ]\n    df[output_cols].to_csv(\"../data/recipes_with_targets.csv\", index=False)\n    print(f\"\\n✓ Dataset guardado: ../data/recipes_with_targets.csv\")
