#!/bin/bash
# Script de arranque para NutriScript AI
# Lanza FastAPI y Streamlit en paralelo

uvicorn app.main:app --host 0.0.0.0 --port 8000 &
streamlit run app/dashboard.py --server.port 8501
