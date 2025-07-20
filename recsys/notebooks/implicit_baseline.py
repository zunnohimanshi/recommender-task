import os
import pandas as pd
import numpy as np
import scipy.sparse as sp
from implicit.als import AlternatingLeastSquares
from tqdm import tqdm

# Avoid OpenBLAS threading issue
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# Load dataset
def load_data(path):
    df = pd.read_csv(os.path.expanduser(path), sep="\t", names=["user_id", "item_id", "rating", "timestamp"])
    return df

# Create sparse interaction matrix (binarized)
def create_interaction_matrix(df):
    user_mapper = {u: i for i, u in enumerate(df['user_id'].unique())}
    item_mapper = {i: j for j, i in enumerate(df['item_id'].unique())}
    user_inverse_mapper = {i: u for u, i in user_mapper.items()}

    user_index = df['user_id'].map(user_mapper)
    item_index = df['item_id'].map(item_mapper)

    # Binarize the ratings for implicit feedback
    interactions = sp.coo_matrix((np.ones(len(df)), (user_index, item_index)))
    return interactions.tocsr(), user_mapper, item_mapper, user_inverse_mapper

# Train-test split
def train_test_split_sparse(matrix, seed=42):
    np.random.seed(seed)
    train_matrix = matrix.copy().tolil()
    test_matrix = sp.lil_matrix(matrix.shape)

    for user in range(matrix.shape[0]):
        items = matrix[user].indices
        if len(items) < 2:
            continue
        test_item = np.random.choice(items)
        train_matrix[user, test_item] = 0
        test_matrix[user, test_item] = 1

    train_matrix = train_matrix.tocsr()
    test_matrix = test_matrix.tocsr()
    print(f"✅ Train interactions: {train_matrix.nnz}, Test interactions: {test_matrix.nnz}")
    return train_matrix, test_matrix

# Evaluation metric: Precision@K
def precision_at_k(model, train_mat, test_mat, k=10):
    precisions = []

    for user_id in tqdm(range(train_mat.shape[0]), desc="Evaluating"):
        test_items = test_mat[user_id].indices
        if len(test_items) == 0:
            continue

        try:
            recommended = model.recommend(user_id, train_mat, N=k, filter_already_liked_items=True)
            recommended_items = [item for item, _ in recommended]

            if not recommended_items:
                continue

            hits = len(set(recommended_items) & set(test_items))
            precisions.append(hits / k)
        except:
            continue

    return np.mean(precisions) if precisions else 0.0

# Main execution
if __name__ == "__main__":
    print("📥 Loading data...")
    df = load_data("~/Desktop/recsys/data/ml-100k/u.data")

    print("📊 Creating interaction matrix...")
    matrix, user_mapper, item_mapper, user_inverse_mapper = create_interaction_matrix(df)
    print(f"✅ User-Item matrix shape: {matrix.shape}")

    print("🧪 Splitting train and test...")
    train_matrix, test_matrix = train_test_split_sparse(matrix)

    print("🤖 Training ALS model...")
    model = AlternatingLeastSquares(factors=50, iterations=20, regularization=0.01)
    model.fit(train_matrix.T)  # Don't convert to CSC, implicit will do that

    print("📈 Evaluating model...")
    precision = precision_at_k(model, train_matrix, test_matrix, k=10)
    print(f"\n🎯 Precision@10: {precision:.4f}")
