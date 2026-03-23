import streamlit as st
import pandas as pd

st.set_page_config(page_title="NutriScript AI Dashboard", layout="wide")
st.title("NutriScript AI Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("../data/recipes_processed.csv")

df = load_data()

st.sidebar.header("Filtros")
nutriscore = st.sidebar.multiselect("Nutri-Score", options=df["nutriscore"].unique())
diet_type = st.sidebar.multiselect("Tipo de Dieta", options=df["diet_type"].unique())
difficulty = st.sidebar.multiselect("Dificultad", options=df["difficulty"].unique())

filtered_df = df.copy()
if nutriscore:
    filtered_df = filtered_df[filtered_df["nutriscore"].isin(nutriscore)]
if diet_type:
    filtered_df = filtered_df[filtered_df["diet_type"].isin(diet_type)]
if difficulty:
    filtered_df = filtered_df[filtered_df["difficulty"].isin(difficulty)]

st.dataframe(filtered_df.head(100))

st.markdown("---")
st.header("Análisis de Recetas")
st.bar_chart(filtered_df["nutriscore"].value_counts())
st.bar_chart(filtered_df["diet_type"].value_counts())
st.bar_chart(filtered_df["difficulty"].value_counts())
