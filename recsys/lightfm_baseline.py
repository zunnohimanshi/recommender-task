import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.sparse import csr_matrix
from lightfm import LightFM
from lightfm.evaluation import precision_at_k, recall_at_k

# Parameters
K = 10
EPOCHS = 20
NO_COMPONENTS = 50
LEARNING_RATE = 0.05

# Load and preprocess
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

def train_test_split(matrix, test_percentage=0.1):
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

def evaluate(model, train_matrix, test_matrix, k):
    print("\n📊 Evaluation Results:")
    precision = precision_at_k(model, test_matrix, train_interactions=train_matrix, k=k).mean()
    recall = recall_at_k(model, test_matrix, train_interactions=train_matrix, k=k).mean()
    
    # Manual NDCG@k
    ndcgs = []
    for user in tqdm(range(test_matrix.shape[0]), desc="Calculating NDCG"):
        scores = model.predict(user, np.arange(test_matrix.shape[1]))
        top_k = np.argsort(-scores)[:k]
        actual = test_matrix[user].indices
        dcg = sum([1.0 / np.log2(i + 2) for i, item in enumerate(top_k) if item in actual])
        idcg = sum([1.0 / np.log2(i + 2) for i in range(min(len(actual), k))])
        ndcg = dcg / idcg if idcg > 0 else 0.0
        ndcgs.append(ndcg)

    print(f"Precision@{k}: {precision:.4f}")
    print(f"Recall@{k}:    {recall:.4f}")
    print(f"NDCG@{k}:      {np.mean(ndcgs):.4f}")

def main():
    print("📥 Loading and preprocessing data...")
    df = load_data("u.data")
    matrix, user_map, item_map = preprocess(df)

    print("🧪 Splitting train/test...")
    train_matrix, test_matrix = train_test_split(matrix)

    print("🧠 Training LightFM model...")
    model = LightFM(no_components=NO_COMPONENTS, loss='warp', learning_rate=LEARNING_RATE)
    model.fit(train_matrix, epochs=EPOCHS, num_threads=4)

    print("✅ Evaluating model...")
    evaluate(model, train_matrix, test_matrix, K)

if __name__ == "__main__":
    main()
