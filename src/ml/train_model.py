import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


# =========================
# 1. Paths
# =========================

X_TRAIN_PATH = "data/processed/X_train.csv"
X_TEST_PATH = "data/processed/X_test.csv"

Y_TRAIN_PATH = "data/processed/y_train.csv"
Y_TEST_PATH = "data/processed/y_test.csv"

MODEL_DIR = "models/ml"

os.makedirs(MODEL_DIR, exist_ok=True)


# =========================
# 2. Load processed data
# =========================

print("Loading processed data...")

X_train = pd.read_csv(X_TRAIN_PATH)
X_test = pd.read_csv(X_TEST_PATH)

y_train = pd.read_csv(Y_TRAIN_PATH).squeeze()
y_test = pd.read_csv(Y_TEST_PATH).squeeze()

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)
print("y_train:", y_train.shape)
print("y_test :", y_test.shape)


# =========================
# 3. Create Random Forest
# =========================

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)


# =========================
# 4. Train model
# =========================

print("Training model...")

model.fit(X_train, y_train)


# =========================
# 5. Save model
# =========================

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "flood_risk_model.joblib"
)

joblib.dump(model, MODEL_PATH)


# =========================
# 6. Finished
# =========================

print("\nModel training completed successfully!")
print("Model saved at:")
print(MODEL_PATH)