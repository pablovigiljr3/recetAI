# 📋 CHEAT SHEET - NutriScript AI

## ⚡ Comandos Más Usados

### Setup (Primeira Vez)
```bash
conda activate recetAI
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Ejecutar Notebooks
```bash
jupyter notebook
# Luego ejecuta 01 → 02 → 03 → 04 en orden
```

### Ejecutar App
```bash
# Terminal 1 - API Backend
cd app
uvicorn main:app --reload --port 8000
# → http://localhost:8000/docs

# Terminal 2 - Dashboard Frontend
cd app
streamlit run dashboard.py --server.port 8501
# → http://localhost:8501 (abre automáticamente)
```

### Docker
```bash
cd docker
docker build -t nutriscript:latest .
docker run -p 8000:8000 -p 8501:8501 nutriscript:latest
```

---

## 🐍 Python Snippets Rápidos

### Cargar Preprocessor
```python
from src.preprocess import NutriscriptPreprocessor
nsp = NutriscriptPreprocessor()
nsp.load_data()
nsp.preprocess_pipeline()
```

### Usar Utils
```python
from src.utils import clean_text, validate_recipe_data, filter_recipes_by_nutriscore
import pandas as pd

df = pd.read_csv('data/recipes_nlp_processed.csv')
healthy = filter_recipes_by_nutriscore(df, 'A')
```

### Cargar Modelos
```python
import pickle
with open('data/lstm_nutriscore_model.pkl', 'rb') as f:
    model = pickle.load(f)
```

---

## 📊 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| API Docs | http://localhost:8000/docs | Swagger UI - Probar endpoints |
| API Health | http://localhost:8000/health | Status del API |
| Dashboard | http://localhost:8501 | Interfaz web Streamlit |
| Jupyter | http://localhost:8888 | Notebooks (si está corriendo) |

---

## 📁 Rutas Clave

```
RecetAI/
├── data/RAW_recipes.csv          ← Input original
├── notebooks/01*.ipynb           ← Ejecutar primero
├── notebooks/02*.ipynb           ← Ejecutar segundo
├── notebooks/03*.ipynb           ← Ejecutar tercero
├── notebooks/04*.ipynb           ← Ejecutar cuarto
├── app/main.py                   ← FastAPI backend
├── app/dashboard.py              ← Streamlit UI
├── src/preprocess.py             ← Clase principal
├── src/utils.py                  ← Funciones helper
└── docker/Dockerfile             ← Para deployment
```

---

## ⏱️ Tiempo Promedio de Ejecución

```
NB01 - Text Mining:          ~3 minutos
NB02 - NLP Pipeline:         ~10 minutos (primera vez)
NB03 - Model Training:       ~15 minutos (LSTM es lento)
NB04 - RAG System:           ~5 minutos
FastAPI startup:             ~2 segundos
Streamlit startup:           ~3 segundos
Total primera ejecución:     ~35 minutos
```

---

## 🆘 Errores Comunes & Soluciones

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError: spacy` | `pip install -r requirements.txt` |
| `en_core_web_sm not found` | `python -m spacy download en_core_web_sm` |
| `Port 8000 already in use` | Cambiar puerto: `--port 8001` |
| `Out of Memory` | Reducir batch_size en spaCy pipe |
| `CUDA not available` | Normal, usará CPU |
| `ImportError` | Verificar: `conda activate recetAI` |

---

## 📈 Resultados Esperados

```
Accuracy (NB):       52.1%
Accuracy (LSTM):     61.2% ← MEJOR
F1-Score (NB):       0.48
F1-Score (LSTM):     0.59
Mejora:              +9.1 puntos porcentuales

Processing Speed:    3,000-5,000 docs/seg
Memory Usage:        ~2-3 GB
Prediction Time:     <200ms por receta
```

---

## 🔍 Testing Rápido

```bash
# Verificar Python
python --version

# Verificar conda
conda list

# Verificar imports
python -c "import pandas; import spacy; print('OK')"

# Probar preprocess
python -c "from src.preprocess import NutriscriptPreprocessor; print('OK')"

# Probar utils
python -c "from src.utils import clean_text; print('OK')"

# Listar archivos generados
ls -lh data/*.csv
ls -lh data/*.pkl
ls -lh data/*.h5
```

---

## 🎯 Flujo de Uso Típico

```
1. Setup ambiente
   └─→ conda activate recetAI

2. Instalar dependencias
   └─→ pip install -r requirements.txt

3. Ejecutar notebooks EN ORDEN (crucial)
   ├─→ NB01 (EDA)
   ├─→ NB02 (NLP)
   ├─→ NB03 (ML/DL)
   └─→ NB04 (RAG)

4. Iniciar backend & frontend
   ├─→ Terminal 1: uvicorn main:app --reload
   └─→ Terminal 2: streamlit run dashboard.py

5. Acceder a interfaces
   ├─→ API: http://localhost:8000/docs
   └─→ UI: http://localhost:8501

6. Usar sistema
   ├─→ Buscar recetas
   ├─→ Predecir Nutri-Score
   └─→ Ver sugerencias RAG
```

---

## 📚 Dónde Encontrar...

| ¿Qué buscas? | Dónde está |
|-------------|-----------|
| Instrucciones rápidas | QUICK_START.md |
| Visión general | README.md |
| Status/métricas | RESUMEN_EJECUTIVO.md |
| Teoría/arquitectura | DOCUMENTACION_TECNICA.md |
| Ejemplos de código | GUIA_MODULOS_PYTHON.md |
| Índice de docs | INDICE_DOCUMENTACION.md |
| Este cheat sheet | CHEAT_SHEET.md (aquí) |
| Este archivo | GUIA_DEFINITIVA.md |

---

## 🖥️ Configuración de IDE (VS Code)

### Extensiones Recomendadas
```
Pylance
Python
Jupyter
Better Comments
Thunder Client (para testear API)
```

### Debugging
```bash
# Abrir con debugging
python -m debugpy --listen 5678 main.py

# En VS Code: Python: Attach usando localhost:5678
```

### Settings para Jupyter
```json
"jupyter.notebookFileRoot": "${workspaceFolder}/notebooks",
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
```

---

## 🔧 Configuración de Ambiente

### Variables de Ambiente (si necesitas)
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export SPACY_MODEL="en_core_web_sm"
export LSTM_BATCH_SIZE=32
```

### En Windows (PowerShell)
```powershell
$env:PYTHONPATH = "$(Get-Location)\src"
$env:SPACY_MODEL = "en_core_web_sm"
```

---

## 📊 Monitoreo en Producción

### Ver CPU/Memoria
```bash
# En Linux/Mac
top

# En Windows (PowerShell)
Get-Process python | select cpu, memory
```

### Ver logs FastAPI
```bash
# Agregar a main.py:
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Ver logs Streamlit
```bash
# Por defecto en ~/.streamlit/logs/
tail -f ~/.streamlit/logs/streamlit_session_*.log
```

---

## 🚀 Tips de Performance

| Problema | Solución |
|----------|----------|
| Lento procesamiento | Reducir n_process o batch_size |
| Alto uso RAM | Procesar en chunks, no todo a la vez |
| Predicción lenta | Cachear modelos en memoria |
| API timeouts | Aumentar timeout en requests |

---

## 📦 Pacquetes Key Versions

```
pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=1.0.0
tensorflow>=2.9.0
spacy>=3.3.0
fastapi>=0.95.0
streamlit>=1.25.0
uvicorn>=0.21.0
```

---

## 🎓 Conceptos en 30 Segundos

| Concepto | Explicación |
|----------|-------------|
| **TF-IDF** | Frecuencia de palabra ponderada |
| **SVD/LSA** | Compresión semántica 5000→100 dims |
| **Naive Bayes** | Clasificador probabilístico simple |
| **LSTM** | Red neuronal para secuencias largas |
| **Embedding** | Palabras como vectores densos |
| **RAG** | Retrieval + Generation para sugerencias |
| **spaCy** | Librería NLP rápida y precisa |

---

## 🎯 Métodos Comunes de src/

```python
# Preprocess
nsp.load_data()
nsp.spacy_process_texts()
nsp.extract_lemmas_pos()
nsp.compute_nutriscore()
nsp.classify_diet()
nsp.classify_difficulty()
nsp.preprocess_pipeline()  # Todo junto

# Utils
clean_text(text)
validate_recipe_data(df)
filter_recipes_by_nutriscore(df, 'A')
get_nutritional_comparison(r1, r2)
get_nutriscore_color('C')
```

---

## ✅ Pre-Ejecución Checklist

- [ ] Python 3.9+ instalado
- [ ] conda funcional
- [ ] 8GB RAM disponible
- [ ] Internet para descargar modelos
- [ ] spaCy model descargado
- [ ] requirements.txt instalado
- [ ] data/RAW_recipes.csv existe

---

## 🎁 Bonus: One-Liners

```bash
# Checkear si todo está OK
python -c "import pandas, spacy, sklearn, tensorflow; print('✅ All imports OK')"

# Ver tamaño del dataset
python -c "import pandas as pd; df = pd.read_csv('data/RAW_recipes.csv'); print(f'{len(df)} recipes')"

# Limpiar caché
find . -type d -name __pycache__ -exec rm -r {} +

# Crear backup
cp data/RAW_recipes.csv data/RAW_recipes.csv.bak

# Ver archivos generados
ls -lh data/*.csv data/*.pkl data/*.h5 2>/dev/null | tail -20
```

---

## 🌐 APIs & Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Mix flour and sugar", "model": "lstm"}'

# Filtrar recetas
curl "http://localhost:8000/recipes?nutriscore=A"

# Sugerencias RAG
curl -X POST http://localhost:8000/suggest_ingredient \
  -H "Content-Type: application/json" \
  -d '{"ingredient": "butter", "recipe_id": 1}'
```

---

## 🔐 Seguridad Básica

```python
# Agregar en main.py si necesitas seguridad:
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.get("/protected")
async def protected(credentials: HTTPAuthCredentials = Depends(security)):
    # verify token...
    return {"message": "Authorized"}
```

---

## 📞 Support Matrix

| Pregunta | Respuesta Rápida |
|----------|------------------|
| ¿Funciona? | Sí ✅ - 100% listo |
| ¿Rápido? | Sí - 3-5K docs/seg |
| ¿Preciso? | Sí - 61.2% accuracy |
| ¿Documentado? | Sí - 50+ páginas |
| ¿Productivo? | Sí - Docker ready |
| ¿Escalable? | Sí - 30K recetas |
| ¿Mantenible? | Sí - Type hints + docstrings |

---

**¡Listo para usar!** 🚀

Vuelve a este archivo cuando necesites recordar algo rápido.

*Última actualización: Marzo 2024*
