# 🐍 Guía de Uso - Módulos Python

Este documento muestra cómo usar cada módulo Python del proyecto de forma programática.

---

## 1. Usar `src/preprocess.py`

### Opción A: Script Autónomo (Recomendado)

Simplemente corre el módulo como script:

```bash
cd src
python preprocess.py
```

Esto ejecutará automáticamente:
1. Carga de datos (RAW_recipes.csv)
2. Procesamiento spaCy (30,000 documentos)
3. Ingeniería de características
4. Guardado de `recipes_nlp_processed.csv`

**Output esperado**:
```
Loading spaCy model...
✓ Model loaded: en_core_web_sm

Loading data from ../data/RAW_recipes.csv...
Found 30000 recipes
Processing texts with spaCy (this may take a few minutes)...
Processing: 100%|████████████████| 30000/30000
✓ Processing completed in 456.23 seconds (65 docs/sec)

Computing Nutri-Scores...
✓ 30000 Nutri-Scores computed

Classifying diets...
✓ 30000 diet types assigned

Classifying difficulties...
✓ 30000 difficulties assigned

Saving output...
✓ Saved to ../data/recipes_nlp_processed.csv (30000 rows)
```

---

### Opción B: Uso Programático en Python

```python
from src.preprocess import NutriscriptPreprocessor

# Crear instancia
nsp = NutriscriptPreprocessor()

# Cargar datos (primera vez, o desde CSV existente)
nsp.load_data()  # Carga RAW_recipes.csv
print(f"Dataset shape: {nsp.df.shape}")  # (30000, 12)

# Procesar con spaCy
nsp.spacy_process_texts()
print(f"Processing complete, added {len(nsp.df.columns)} columns")

# Extraer features NLP
lemmas_df = nsp.extract_lemmas_pos()
print(f"Lemmas extracted: {len(lemmas_df)}")

# Computar targets
nsp.compute_nutriscore()
nsp.classify_diet()
nsp.classify_difficulty()

# Pipeline completo de una vez
nsp.preprocess_pipeline()

# Guardar resultados
nsp.df.to_csv('../data/recipes_processed.csv', index=False)
```

---

### Opción C: Customizar Parámetros

```python
from src.preprocess import NutriscriptPreprocessor

# Instancia con parámetros personalizados
nsp = NutriscriptPreprocessor()

# Cargar solo primeras 5000 recetas
nsp.load_data(sample_size=5000)

# Procesar con batch_size más pequeño (para máquinas con poca RAM)
texts = nsp.df['steps'].values
nsp.nlp.pipe(texts, n_process=-1, batch_size=500)

# Usar modelo más completo de spaCy (más lento, más preciso)
# nsp.nlp = spacy.load("en_core_web_md")  # En lugar de web_sm

print(nsp.df.head())
```

---

## 2. Usar `src/utils.py`

### Importar y Usar Funciones Individuales

```python
from src.utils import *
import pandas as pd

# Cargar dataset procesado
df = pd.read_csv('../data/recipes_nlp_processed.csv')

# 1. Limpiar texto
text = "Hello, WORLD!!!  This is a TEST."
cleaned = clean_text(text, lowercase=True, remove_punctuation=True)
print(cleaned)  # "hello world this is a test"

# 2. Validar integridad de datos
issues = validate_recipe_data(df)
if issues:
    print(f"⚠️ Issues found: {issues}")
else:
    print("✅ Data integrity OK")

# 3. Filtrar recetas por Nutri-Score
healthy = filter_recipes_by_nutriscore(df, nutriscore='A')
print(f"Found {len(healthy)} recipes with Nutri-Score A")

# 4. Filtrar por dificultad
easy = filter_recipes_by_difficulty(df, difficulty='Easy')
print(f"Found {len(easy)} easy recipes")

# 5. Comparar nutrición entre 2 recetas
recipe1 = df.iloc[0]
recipe2 = df.iloc[1]
comparison = get_nutritional_comparison(recipe1, recipe2)
print(comparison)
# Output:
# {
#   'calories_diff': 150,
#   'sugar_diff': -5.2,
#   'sat_fat_diff': 3.1,
#   'protein_diff': 2.0
# }

# 6. Obtener color para Nutri-Score
color_a = get_nutriscore_color('A')  # '#4CAF50' (verde)
color_e = get_nutriscore_color('E')  # '#F44336' (rojo)
print(f"Color for A: {color_a}, Color for E: {color_e}")

# 7. Descripción de Nutri-Score
desc = get_nutriscore_description('C')
print(desc)  # "Moderate - Some nutritional improvements recommended"
```

---

## 3. Usar `src/train.py` (Si existe)

```python
from src.train import train_models, evaluate_models
import pandas as pd
from sklearn.model_selection import train_test_split

# Cargar datos procesados
df = pd.read_csv('../data/recipes_nlp_processed.csv')

# Preparar X (features) y y (target)
X = df.drop('nutriscore', axis=1)  # Features
y = df['nutriscore']  # Target

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entrenar
models = train_models(X_train, y_train)

# Evaluar
results = evaluate_models(models, X_test, y_test)
print(results)
# Output: {'naive_bayes': 0.521, 'lstm': 0.612, ...}
```

---

## 4. Usar `src/rag_assistant.py` (Si existe)

```python
from src.rag_assistant import RAGAssistant
import pandas as pd

# Cargar dataset
df = pd.read_csv('../data/recipes_nlp_processed.csv')

# Inicializar RAG
rag = RAGAssistant(df)

# Ejemplo 1: Buscar alternativas saludables para un ingrediente
suggestions = rag.suggest_healthy_ingredient(
    ingredient='butter',
    top_k=5,
    min_nutriscore='A'
)
print(suggestions)
# Output: ['olive oil', 'coconut oil', 'avocado oil', ...]

# Ejemplo 2: Encontrar recetas similares
similar = rag.find_similar_recipes(
    recipe_id=100,
    top_k=3
)
print(similar)
# Output: [(103, 0.89), (105, 0.87), (108, 0.84)]

# Ejemplo 3: Analizar una receta
analysis = rag.analyze_recipe(recipe_id=100)
print(analysis)
# Output: {
#   'nutriscore': 'D',
#   'issues': ['high sugar', 'high sat_fat'],
#   'suggestions': ['reduce sugar', 'use olive oil']
# }
```

---

## 5. Testing Individual Module

### Test Preprocess

```bash
# Verificar que preprocess.py funciona
python -c "
from src.preprocess import NutriscriptPreprocessor
nsp = NutriscriptPreprocessor()
print('✅ NutriscriptPreprocessor imported successfully')
"
```

### Test Utils

```bash
# Verificar que utils.py funciona
python -c "
from src.utils import clean_text, validate_recipe_data
text = clean_text('Hello WORLD!!!', lowercase=True)
print(f'✅ clean_text works: {text}')
"
```

---

## 6. Usar en Jupyter Notebooks

Si quieres integrar los módulos en los notebooks:

```python
# Al inicio del notebook
import sys
sys.path.insert(0, '../src')  # Agregar src al path

from preprocess import NutriscriptPreprocessor
from utils import *
import pandas as pd

# Ahora puedes usar:
nsp = NutriscriptPreprocessor()
nsp.load_data()
# ... resto del código
```

---

## 7. Debugging y Logging

### Habilitar Logs Detallados

```python
import logging
from src.preprocess import NutriscriptPreprocessor

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Ahora verás más detalles durante ejecución
nsp = NutriscriptPreprocessor()
nsp.preprocess_pipeline()
```

### Debugging de Errores

```python
from src.preprocess import NutriscriptPreprocessor
import traceback

try:
    nsp = NutriscriptPreprocessor()
    nsp.load_data()
    nsp.spacy_process_texts()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()  # Ver stack trace
```

---

## 8. Integración con FastAPI

```python
# En app/main.py
from fastapi import FastAPI
from src.preprocess import NutriscriptPreprocessor
from src.utils import validate_recipe_data
import pandas as pd

app = FastAPI()

# Cargar modelo al iniciar
@app.on_event("startup")
async def startup():
    global nsp
    nsp = NutriscriptPreprocessor()
    nsp.load_data()
    print("✅ Models loaded")

@app.get("/predict")
async def predict(text: str):
    # Usar módulo preprocess
    result = nsp.process_single_recipe(text)
    return {"prediction": result}

@app.get("/validate")
async def validate():
    # Usar módulo utils
    df = pd.read_csv('../data/recipes_nlp_processed.csv')
    issues = validate_recipe_data(df)
    return {"status": "ok" if not issues else "error", "issues": issues}
```

---

## 9. Integración con Streamlit

```python
# En app/dashboard.py
import streamlit as st
from src.preprocess import NutriscriptPreprocessor
from src.utils import get_nutriscore_color
import pandas as pd

# Cargar datos (con caching)
@st.cache_resource
def load_preprocessor():
    nsp = NutriscriptPreprocessor()
    nsp.load_data()
    return nsp

nsp = load_preprocessor()

# UI
st.title("NutriScript AI Dashboard")
target_score = st.selectbox("Filter by Nutri-Score", ['A', 'B', 'C', 'D', 'E'])

# Usar módulo
color = get_nutriscore_color(target_score)
st.markdown(f"<p style='color: {color}'>Selected: {target_score}</p>", 
            unsafe_allow_html=True)
```

---

## 10. Cheat Sheet

```python
# Imports rápidos
from src.preprocess import NutriscriptPreprocessor
from src.utils import (
    clean_text, validate_recipe_data, 
    filter_recipes_by_nutriscore, 
    get_nutritional_comparison,
    get_nutriscore_color
)

# Uso rápido
nsp = NutriscriptPreprocessor()                    # Crear instancia
nsp.load_data()                                    # Cargar CSV
nsp.preprocess_pipeline()                          # Procesar todo
df = nsp.df                                        # Acceder a DataFrame
nsp.df.to_csv('output.csv', index=False)          # Guardar

# Utils
clean_text(text)                                   # Limpiar
validate_recipe_data(df)                           # Validar
filter_recipes_by_nutriscore(df, 'A')             # Filtrar
get_nutritional_comparison(recipe1, recipe2)      # Comparar
get_nutriscore_color('C')                          # Color
```

---

## 11. Ejemplos Avanzados

### Procesar Solo Ingredientes Específicos

```python
from src.preprocess import NutriscriptPreprocessor
from src.utils import filter_recipes_by_nutriscore

nsp = NutriscriptPreprocessor()
nsp.load_data()
nsp.preprocess_pipeline()

# Recetas saludables con pocos pasos
healthy_easy = nsp.df[
    (nsp.df['nutriscore'] == 'A') & 
    (nsp.df['n_steps'] <= 5)
]
print(f"Found {len(healthy_easy)} healthy & easy recipes")
```

### Batch Processing

```python
from src.preprocess import NutriscriptPreprocessor
import pandas as pd

nsp = NutriscriptPreprocessor()

# Procesar en chunks para ahorrar memoria
chunk_size = 5000
for i in range(0, 30000, chunk_size):
    nsp.load_data(sample_size=chunk_size)
    nsp.preprocess_pipeline()
    nsp.df.to_csv(f'../data/chunk_{i}.csv', index=False)
    print(f"✓ Processed chunk {i}-{i+chunk_size}")
```

---

**¡Listo para usar los módulos!** 🚀

Puedes ejecutar cualquiera de estos ejemplos en:
- Terminal directamente: `python script.py`
- Jupyter notebook: `%run script.py`
- En la aplicación web (FastAPI/Streamlit)
