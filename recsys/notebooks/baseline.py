import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse

# 1. Load the dataset
print("📦 Loading data...")
df = pd.read_csv('../data/ml-100k/u.data', sep='\t', names=['userId', 'itemId', 'rating', 'timestamp'])

# 2. Prepare the dataset for Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userId', 'itemId', 'rating']], reader)

# 3. Train-test split
print("✂️ Splitting train/test...")
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# 4. Initialize the model
print("🧠 Training SVD model...")
model = SVD()
model.fit(trainset)

# 5. Evaluate the model
print("📊 Evaluating on test set...")
predictions = model.test(testset)

# 6. Calculate RMSE
error = rmse(predictions)
print(f"✅ RMSE: {error:.4f}")

# 7. Show a few predictions
print("\n🔮 Sample predictions:")
for pred in predictions[:5]:
    print(f"User {pred.uid} - Item {pred.iid} | Actual: {pred.r_ui}, Predicted: {pred.est:.2f}")
