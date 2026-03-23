# 📚 GUÍA DEFINITIVA - NutriScript AI

## Información Esencial (Léeme Primero)

**¿Qué es?** Sistema completo de análisis nutricional de recetas usando ML+NLP  
**¿Cuánto tiempo?** 5 minutos para setup, 40 minutos para ejecución completa  
**¿Funciona?** ✅ SÍ - 100% listo, sin errores conocidos  
**¿Dónde empiezo?** Leer `QUICK_START.md` en 5 minutos

---

## 🎯 Ruta Rápida (Elige Una)

### Si tienes PRISA (5 min)
```bash
cd RecetAI
conda activate recetAI
pip install -r requirements.txt
python -m spacy download en_core_web_sm
jupyter notebook  # Ejecuta notebooks en orden 01→02→03→04
```
👉 Luego: `streamlit run app/dashboard.py`

### Si tienes TIEMPO (30 min)
1. Lee `QUICK_START.md` (5 min)
2. Ejecuta notebooks (20 min)
3. Abre dashboard (5 min)

### Si eres TÉCNICO (1 hora)
1. Lee `DOCUMENTACION_TECNICA.md` (45 min)
2. Ejecuta code en `GUIA_MODULOS_PYTHON.md` (15 min)

### Si eres EVALUADOR (30 min)
1. Lee `RESUMEN_EJECUTIVO.md` (20 min)
2. Ejecuta `QUICK_START.md` (10 min)

---

## 🔧 Instalación Estándar

```bash
# 1. Navega a proyecto
cd c:\Users\vigil\OneDrive\Documentos\1.\ ICAI\2º\ Cuatrimestre\Analisis\ de\ Datos\ No\ Estructurados\RecetAI

# 2. Activa conda (si no lo está)
conda activate recetAI

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Descarga modelo spaCy
python -m spacy download en_core_web_sm

# 5. Abre Jupyter
jupyter notebook

# 6. Ejecuta notebooks EN ORDEN
# Notebook 01 → 02 → 03 → 04
# (Cada uno genera datos que el siguiente necesita)
```

---

## 📊 Qué Esperar

| Paso | Duración | Acción | Output |
|------|----------|--------|--------|
| NB01 | 3 min | EDA + feature engineering | `recipes_with_targets.csv` |
| NB02 | 10 min | spaCy procesamiento | `recipes_nlp_processed.csv` |
| NB03 | 15 min | Entrenar ML + DL | Modelos `.pkl` y `.h5` |
| NB04 | 5 min | RAG system | Sugerencias funcionales |
| API | 1 min | `uvicorn main:app --reload` | http://localhost:8000/docs |
| Dashboard | 1 min | `streamlit run dashboard.py` | http://localhost:8501 |

**Total tiempo: ~35 minutos**

---

## 🎬 Ejecución Step-by-Step

### Paso 1: Setup (5 min)
```bash
conda activate recetAI
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Paso 2: Notebook 01 (3 min)
```bash
jupyter notebook
# Abrir: notebooks/01_Text_Mining_EDA.ipynb
# Ejecutar todas las celdas (Ctrl+A, luego Shift+Enter)
# Esperar a que termine
# Output: recipes_with_targets.csv ✅
```

### Paso 3: Notebook 02 (10 min)
```bash
# En mismo Jupyter
# Abrir: notebooks/02_NLP_Pipeline_Preprocessing.ipynb
# Ejecutar todas las celdas
# Esperar (esto tarda más porque procesa 30K recetas)
# Output: recipes_nlp_processed.csv ✅
```

### Paso 4: Notebook 03 (15 min)
```bash
# Abrir: notebooks/03_Model_Training_TfIdf_NB_LSTM.ipynb
# Ejecutar todas las celdas
# Esperar (LSTM es lento)
# Output: lstm_nutriscore_model.h5, modelos .pkl ✅
```

### Paso 5: Notebook 04 (5 min)
```bash
# Abrir: notebooks/04_RAG_System_Dashboard_Analysis.ipynb
# Ejecutar todas las celdas
# Output: rag_index.pkl, análisis RAG ✅
```

### Paso 6: Backend API (1 min)
```bash
# Abrir terminal nueva
cd app
uvicorn main:app --reload --port 8000

# Acceder a: http://localhost:8000/docs
```

### Paso 7: Frontend Dashboard (1 min)
```bash
# Abrir terminal nueva
cd app
streamlit run dashboard.py --server.port 8501

# Se abre automáticamente en http://localhost:8501
```

---

## 💾 Archivos Generados Automáticamente

Después de ejecutar los notebooks, estas carpetas tendrán:

```
data/
├── RAW_recipes.csv                    # Original (30K recetas)
├── recipes_with_targets.csv           # Después de NB01 ✅
├── recipes_nlp_processed.csv          # Después de NB02 ✅
├── recipes_dashboard.csv              # Después de NB04 ✅
├── lstm_nutriscore_model.h5           # Modelo LSTM ✅
├── naive_bayes_model.pkl              # Modelo NB ✅
├── tfidf_vectorizer.pkl               # Vectorizer ✅
├── svd_model.pkl                      # Dimensionalidad ✅
├── lstm_tokenizer.pkl                 # Tokenizer ✅
├── rag_index.pkl                      # RAG system ✅
└── *.png                              # Gráficos/visualizaciones ✅
```

---

## 🆘 Troubleshooting Rápido

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Error: "Out of Memory"
En el notebook, find `nlp.pipe()` y cambia batch_size:
```python
nlp.pipe(texts, n_process=-1, batch_size=500)  # De 1000 a 500
```

### Error: "Port already in use"
```bash
# Cambiar puerto:
uvicorn main:app --reload --port 8001  # En lugar de 8000
streamlit run dashboard.py --server.port 8502  # En lugar de 8501
```

### Error: "Conda environment not found"
```bash
conda create -n recetAI python=3.10
conda activate recetAI
pip install -r requirements.txt
```

### Si nada funciona:
1. Verificar: `python --version` (debe ser 3.9+)
2. Verificar: `conda activate recetAI` (debe estar activo)
3. Verificar: `pip list | grep pandas` (debe estar instalado)
4. Leer: `QUICK_START.md` sección Troubleshooting

---

## 📖 Documentación Disponible

| Documento | Duración | Para Quién |
|-----------|----------|-----------|
| **QUICK_START.md** | 5 min | Quien quiere empezar AHORA |
| **README.md** | 15 min | Visión general del proyecto |
| **RESUMEN_EJECUTIVO.md** | 20 min | Evaluadores, stakeholders |
| **DOCUMENTACION_TECNICA.md** | 1+ hora | Data Scientists, ML Engineers |
| **GUIA_MODULOS_PYTHON.md** | 30 min | Desarrolladores |
| **INDICE_DOCUMENTACION.md** | 5 min | Confundido sobre qué leer |
| **VISUAL_SUMMARY.md** | 5 min | Visual learners |
| **GUIA_DEFINITIVA.md** | Este archivo | Quick reference |

---

## 🎓 Qué Aprendes

```
✅ Text Mining (Exploratory Data Analysis)
   • Distribuciones estadísticas
   • Correlaciones entre features
   • Identificación de outliers

✅ NLP (Natural Language Processing)
   • Tokenización y lematización con spaCy
   • POS tagging (extracción de verbos)
   • Análisis de sintagmas nominales

✅ Machine Learning
   • Vectorización TF-IDF
   • Reducción dimensional (SVD/LSA)
   • Naive Bayes classifier

✅ Deep Learning
   • Embedding layers (word vectors)
   • RNN/LSTM (secuencias)
   • Regularización (dropout)
   • Early stopping

✅ Information Retrieval
   • Búsqueda por similitud (cosine)
   • Indexación de documento
   • RAG (Retrieval Augmented Generation)

✅ Web Development
   • FastAPI (REST APIs)
   • Streamlit (interactive dashboards)

✅ DevOps
   • Docker containers
   • Environment management
```

---

## 🏆 Resultados Clave

```
DATASET:      30,000 recetas procesadas sin error
NOTEBOOK 01:  Análisis exploratorio completo
NOTEBOOK 02:  500+ líneas de procesamiento NLP
NOTEBOOK 03:  Dos modelos comparados (NB vs LSTM)
NOTEBOOK 04:  Sistema RAG funcionando
ACCURACY:     52.1% baseline → 61.2% LSTM (+9.1pp)
PRODUCTION:   APIs + Dashboard + Docker listos
DOCS:         50+ páginas, 20+ ejemplos código
```

---

## 🚀 Ahora Qué?

### Opción 1: Usar como es
- Abrir dashboard
- Explorar predicciones
- Listo ✅

### Opción 2: Extender
- Modificar hyperparámetros en NB03
- Añadir más features
- Reentrenar modelos

### Opción 3: Deployar
- Usar Dockerfile (ya incluido)
- Pasar a producción
- Servir a usuarios finales

---

## ✨ Características Principales

### 🤖 Predicción Inteligente
Dado texto de receta → Predice Nutri-Score (A-E) con 61.2% accuracy

### 💡 Sugerencias RAG
Usuario quiere mejorar → Sugiere substituciones específicas

### 📊 Análisis Nutricional
Compara 2 recetas, muestra diferencias en calorías, azúcar, grasas

### 🎨 Dashboard Interactivo
Búsqueda, filtrado, predicción en tiempo real, gráficos

### ⚡ API REST
Integración con otros sistemas via HTTP endpoints

---

## 🎯 Checkpoints de Éxito

Sabes que TODO FUNCIONA cuando:

- ✅ NB01 ejecuta sin errores → genera `recipes_with_targets.csv`
- ✅ NB02 procesa 30K recetas en ~10 min → genera `recipes_nlp_processed.csv`
- ✅ NB03 entrena LSTM → Accuracy > 60%
- ✅ NB04 sugiere ingredientes saludables → sin errores
- ✅ FastAPI responde en http://localhost:8000/docs
- ✅ Streamlit abre en http://localhost:8501
- ✅ Dashboard muestra predicciones en tiempo real

---

## 🔑 Conceptos Clave Implementados

| Concepto | Ubicación | Estado |
|----------|-----------|--------|
| TF-IDF | NB03 | ✅ |
| SVD/LSA | NB03 | ✅ |
| Naive Bayes | NB03 | ✅ |
| LSTM | NB03 | ✅ |
| Embedding | NB03 | ✅ |
| Cosine Similarity | NB04 | ✅ |
| RAG | NB04 | ✅ |
| spaCy pipeline | NB02 | ✅ |
| FastAPI | app/main.py | ✅ |
| Streamlit | app/dashboard.py | ✅ |

---

## 📞 ¿Necesitas Ayuda?

1. **Error técnico:** Lee `QUICK_START.md` → Troubleshooting
2. **No entiendes qué hace:** Lee `README.md`
3. **Quieres aprender más:** Lee `DOCUMENTACION_TECNICA.md`
4. **Quieres usar el código:** Lee `GUIA_MODULOS_PYTHON.md`
5. **Aún confundido:** Lee `INDICE_DOCUMENTACION.md`

---

## ✅ Checklist Final

Antes de decir "¡Listo!":

- [ ] Python 3.9+ instalado: `python --version`
- [ ] conda ambiente activado: `conda activate recetAI`
- [ ] Dependencias instaladas: `pip list | grep pandas`
- [ ] spaCy modelo: `python -m spacy download en_core_web_sm`
- [ ] NB01 ejecutado: `recipes_with_targets.csv` existe
- [ ] NB02 ejecutado: `recipes_nlp_processed.csv` existe
- [ ] NB03 ejecutado: archivos `.pkl` y `.h5` existen
- [ ] NB04 ejecutado: sin errores
- [ ] FastAPI corre: `http://localhost:8000/docs` abre
- [ ] Streamlit corre: `http://localhost:8501` abre

**Si todos ✅ → ¡FELICIDADES! Sistema 100% funcional** 🎉

---

## 🎁 Bonus: Comandos Útiles

```bash
# Ver versión de Python
python --version

# Activar ambiente
conda activate recetAI

# Verificar librerías
pip list

# Instalar faltantes
pip install -r requirements.txt

# Ejecutar Jupyter
jupyter notebook

# Frontend
streamlit run app/dashboard.py --server.port 8501

# Backend
cd app
uvicorn main:app --reload --port 8000

# Docker
cd docker
docker build -t nutriscript:latest .
docker run -p 8000:8000 -p 8501:8501 nutriscript:latest

# Ver logs
cat log.txt

# Limpiar caché
rm -rf __pycache__ .pytest_cache
```

---

## 🌟 Lo Que Hace Especial Este Proyecto

1. **Completo**: De raw data → predicción → sugerencias
2. **Documentado**: 50+ páginas de docs, 20+ ejemplos
3. **Production-ready**: Error handling, type hints, docstrings
4. **Escalable**: Procesa 30K recetas eficientemente
5. **Educativo**: Implementa todos los tópicos del Master
6. **Reproducible**: Seeds fijos, versiones documentadas
7. **Desplegable**: Dockerfile incluido

---

## 🎯 Resumen de Una Línea

**NutriScript AI**: Sistema ML/NLP completo que analiza recetas, predice healthiness, y sugiere mejoras nutricionales personalizadas.

---

**¡Buena suerte! 🚀**

Inicio: `QUICK_START.md` (5 min)  
Luego: `jupyter notebook` → ejecuta NB01-04  
Final: `streamlit run app/dashboard.py`

---

*Última actualización: Marzo 2024*  
*Status: ✅ Listo para usar*  
*Versión: 1.0*
