import os
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.sparse import csr_matrix
from implicit.als import AlternatingLeastSquares

# Prevent OpenBLAS threading issues
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# ----------------- Parameters -----------------
K = 10
FACTORS = 50
ITERATIONS = 20
REGULARIZATION = 0.01

# ----------------- Load & Preprocess -----------------
def load_data(path):
    df = pd.read_csv(path, sep="\t", names=["user", "item", "rating", "timestamp"])
    return df

def preprocess(df):
    user_map = {id: idx for idx, id in enumerate(df['user'].unique())}
    item_map = {id: idx for idx, id in enumerate(df['item'].unique())}

    df['user_idx'] = df['user'].map(user_map)
    df['item_idx'] = df['item'].map(item_map)

    shape = (len(user_map), len(item_map))
    matrix = csr_matrix((df['rating'], (df['user_idx'], df['item_idx'])), shape=shape)
    return matrix, user_map, item_map

# ----------------- Train/Test Split -----------------
def train_test_split_implicit(matrix, test_percentage=0.1):
    matrix = matrix.tolil()
    train = matrix.copy()
    test = csr_matrix(matrix.shape)

    for user in range(matrix.shape[0]):
        items = matrix.rows[user]
        if len(items) == 0:
            continue
        test_size = max(1, int(len(items) * test_percentage))
        test_items = np.random.choice(items, size=test_size, replace=False)
        for item in test_items:
            train[user, item] = 0
            test[user, item] = matrix[user, item]

    return train.tocsr(), test.tocsr()

# ----------------- Evaluation Metrics -----------------
def precision_at_k(recommended, actual, k):
    if not actual:
        return 0.0
    return len(set(recommended[:k]) & set(actual)) / k

def recall_at_k(recommended, actual, k):
    if not actual:
        return 0.0
    return len(set(recommended[:k]) & set(actual)) / len(actual)

def ndcg_at_k(recommended, actual, k):
    dcg = 0.0
    idcg = sum([1.0 / np.log2(i + 2) for i in range(min(len(actual), k))])
    for i, rec in enumerate(recommended[:k]):
        if rec in actual:
            dcg += 1.0 / np.log2(i + 2)
    return dcg / idcg if idcg > 0 else 0.0

# ----------------- Model Evaluation -----------------
def evaluate(model, train_matrix, test_matrix, k=10):
    precisions, recalls, ndcgs = [], [], []

    for user in tqdm(range(train_matrix.shape[0]), desc="Evaluating"):
        actual = test_matrix[user].indices.tolist()
        if len(actual) == 0:
            continue

        recommended = model.recommend(
            userid=user,
            user_items=train_matrix[user],
            N=k,
            filter_already_liked_items=True,
            recalculate_user=True
        )

        # ✅ FINAL SAFE FIX
        recommended_items = [int(row[0]) for row in recommended]

        precisions.append(precision_at_k(recommended_items, actual, k))
        recalls.append(recall_at_k(recommended_items, actual, k))
        ndcgs.append(ndcg_at_k(recommended_items, actual, k))

    print("\n📊 Evaluation Results:")
    print(f"Precision@{k}: {sum(precisions)/len(precisions):.4f}")
    print(f"Recall@{k}:    {sum(recalls)/len(recalls):.4f}")
    print(f"NDCG@{k}:      {sum(ndcgs)/len(ndcgs):.4f}")

# ----------------- Main -----------------
def main():
    print("📥 Loading and preprocessing data...")
    df = load_data("u.data")
    matrix, user_map, item_map = preprocess(df)

    print("🧪 Splitting train/test...")
    train_matrix, test_matrix = train_test_split_implicit(matrix)

    print("🧠 Training ALS model...")
    model = AlternatingLeastSquares(factors=FACTORS,
                                    iterations=ITERATIONS,
                                    regularization=REGULARIZATION)
    model.fit(train_matrix)

    print("✅ Evaluating model...")
    evaluate(model, train_matrix, test_matrix, K)

if __name__ == "__main__":
    main()