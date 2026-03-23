"""
Script de entrenamiento para NutriScript AI
Incluye:
- Representación TF-IDF + SVD (LSA)
- Entrenamiento de Naive Bayes (baseline)
- Entrenamiento de LSTM (deep learning)
- Evaluación y comparación de modelos
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Carga de datos preprocesados
df = pd.read_csv("../data/recipes_processed.csv")

# Representación TF-IDF + SVD (LSA)
vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = vectorizer.fit_transform(df["lemmas"].astype(str))
svd = TruncatedSVD(n_components=100, random_state=42)
X_lsa = svd.fit_transform(X_tfidf)

y = df["nutriscore"].fillna("C")  # Target principal

# Split
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(X_lsa, y, test_size=test_size, random_state=42, stratify=y)

# Baseline: Naive Bayes
nb = MultinomialNB()
nb.fit(X_train, y_train)
y_pred_nb = nb.predict(X_test)
print("--- Naive Bayes ---")
print(classification_report(y_test, y_pred_nb))

# LSTM: Deep Learning
max_words = 5000
max_len = 100

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(df["lemmas"].astype(str))
X_seq = tokenizer.texts_to_sequences(df["lemmas"].astype(str))
X_pad = pad_sequences(X_seq, maxlen=max_len)

X_train_dl, X_test_dl, y_train_dl, y_test_dl = train_test_split(X_pad, y, test_size=test_size, random_state=42, stratify=y)

model = Sequential()
model.add(Embedding(max_words, 128, input_length=max_len))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(5, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Codificar etiquetas Nutri-Score (A-E) a 0-4
y_train_enc = y_train_dl.map({"A":0, "B":1, "C":2, "D":3, "E":4}).values

y_test_enc = y_test_dl.map({"A":0, "B":1, "C":2, "D":3, "E":4}).values

model.fit(X_train_dl, y_train_enc, epochs=5, batch_size=128, validation_data=(X_test_dl, y_test_enc), verbose=2)

loss, acc = model.evaluate(X_test_dl, y_test_enc, verbose=0)
print(f"\n--- LSTM Test Accuracy: {acc:.3f} ---")
