# app.py

import streamlit as st
import numpy as np
from lightfm import LightFM
from lightfm.datasets import fetch_movielens
from implicit.als import AlternatingLeastSquares

import scipy.sparse as sp

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommender System (ALS & LightFM)")

@st.cache_data
def load_data():
    from sklearn.model_selection import train_test_split
    data = fetch_movielens(min_rating=4.0)
    return data['train'], data['test'], data['item_labels']
@st.cache_resource
def train_models(_train):
    als_model = AlternatingLeastSquares(factors=20, regularization=0.1, iterations=20)
    als_model.fit(_train.T)

    lightfm_model = LightFM(no_components=20, loss='warp')
    lightfm_model.fit(_train, epochs=10, num_threads=2)

    return als_model, lightfm_model

train, test, item_labels = load_data()
als_model, lightfm_model = train_models(train)

# UI elements
model_choice = st.selectbox("Choose a model:", ["ALS", "LightFM"])
user_id = st.number_input("Enter a user ID (0 to 942)", min_value=0, max_value=942, value=1)

if st.button("Recommend"):
    if model_choice == "ALS":
        recommended = als_model.recommend(user_id, train[user_id], N=10)
        recommended_ids = [r[0] for r in recommended]
    else:
        scores = lightfm_model.predict(user_id, np.arange(train.shape[1]))
        recommended_ids = np.argsort(-scores)[:10]

    st.subheader("Top 10 Recommended Movies:")
    for i, movie_id in enumerate(recommended_ids, 1):
        st.write(f"{i}. {item_labels[movie_id]}")
