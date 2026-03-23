# ⚡ Quick Start - En 5 Minutos

## Paso 1: Preparar Ambiente (2 min)

```bash
# Navega al proyecto
cd c:\Users\vigil\OneDrive\Documentos\1.\ ICAI\2º\ Cuatrimestre\Analisis\ de\ Datos\ No\ Estructurados\RecetAI

# Activar conda (si no está activo)
conda activate recetAI

# Instalar/actualizar dependencias
pip install -r requirements.txt

# Descargar modelo spaCy (si no lo tienes)
python -m spacy download en_core_web_sm
```

---

## Paso 2: Ejecutar Notebooks (2 min)

```bash
# Abre Jupyter
jupyter notebook
```

**Orden de ejecución** (ejecuta celdas de arriba hacia abajo):

1. **`notebooks/01_Text_Mining_EDA.ipynb`** 
   - Genera `recipes_with_targets.csv`
   - Duración: ~3 min

2. **`notebooks/02_NLP_Pipeline_Preprocessing.ipynb`**
   - Genera `recipes_nlp_processed.csv`
   - Duración: ~10 min (primera vez)

3. **`notebooks/03_Model_Training_TfIdf_NB_LSTM.ipynb`**
   - Entrena modelos ML/DL
   - Duración: ~15 min (LSTM es lento)

4. **`notebooks/04_RAG_System_Dashboard_Analysis.ipynb`**
   - Sistema RAG funcionando
   - Duración: ~5 min

---

## Paso 3: Usar la App (1 min)

### Opción A: API REST
```bash
cd app
uvicorn main:app --reload --port 8000
```
👉 Visita: **http://localhost:8000/docs**

### Opción B: Dashboard Web
```bash
cd app
streamlit run dashboard.py --server.port 8501
```
👉 Visita: **http://localhost:8501**

---

## ✅ Verificación

Si ves esto = **TODO FUNCIONA** ✨

- Notebooks ejecutados sin errores
- API responde en http://localhost:8000/docs
- Dashboard abre en http://localhost:8501

---

## 🆘 Si Algo Falla

**Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Error: "Out of memory"**
En el notebook, busca `nlp.pipe()` y cambia:
```python
nlp.pipe(texts, n_process=-1, batch_size=500)  # Reducir batch_size
```

**Error: "Port already in use"**
```bash
# Cambiar puerto:
uvicorn main:app --reload --port 8001  # En lugar de 8000
streamlit run dashboard.py --server.port 8502  # En lugar de 8501
```

---

## 📚 Documentación Completa

- 📖 **`README.md`** → Más detalles, todos los features
- 📘 **`DOCUMENTACION_TECNICA.md`** → Matemáticas, arquitectura, decisiones

---

**¡Tu sistema está listo!** 🎉
