import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


# =========================
# 1. File paths
# =========================

RAW_FILE = "data/raw/flood_risk_dataset_india.csv"

PROCESSED_DIR = "data/processed"
MODEL_DIR = "models/ml"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


# =========================
# 2. Load dataset
# =========================

print("Loading dataset...")

df = pd.read_csv(RAW_FILE)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())


# =========================
# 3. Target column
# =========================

TARGET = "Flood Occurred"

if TARGET not in df.columns:
    raise ValueError(f"Target column '{TARGET}' not found!")

X = df.drop(columns=[TARGET])
y = df[TARGET].astype(int)


# =========================
# 4. Feature types
# =========================

categorical_features = [
    "Land Cover",
    "Soil Type"
]

numeric_features = [
    "Latitude",
    "Longitude",
    "Rainfall (mm)",
    "Temperature (°C)",
    "Humidity (%)",
    "River Discharge (m³/s)",
    "Water Level (m)",
    "Elevation (m)",
    "Population Density",
    "Historical Floods",
    "Infrastructure"
]


# =========================
# 5. Check columns
# =========================

required_columns = categorical_features + numeric_features

missing_columns = [
    column for column in required_columns
    if column not in X.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# =========================
# 6. Train/Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTrain shape:", X_train.shape)
print("Test shape:", X_test.shape)


# =========================
# 7. Preprocessing
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# =========================
# 8. Fit ONLY on training data
# =========================

print("\nFitting preprocessor...")

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)


# =========================
# 9. Feature names
# =========================

feature_names = preprocessor.get_feature_names_out()

X_train_processed = pd.DataFrame(
    X_train_processed,
    columns=feature_names
)

X_test_processed = pd.DataFrame(
    X_test_processed,
    columns=feature_names
)


# =========================
# 10. Save processed data
# =========================

X_train_processed.to_csv(
    f"{PROCESSED_DIR}/X_train.csv",
    index=False
)

X_test_processed.to_csv(
    f"{PROCESSED_DIR}/X_test.csv",
    index=False
)

y_train.to_csv(
    f"{PROCESSED_DIR}/y_train.csv",
    index=False
)

y_test.to_csv(
    f"{PROCESSED_DIR}/y_test.csv",
    index=False
)


# =========================
# 11. Save preprocessor
# =========================

joblib.dump(
    preprocessor,
    f"{MODEL_DIR}/preprocessor.joblib"
)


# =========================
# 12. Final information
# =========================

print("\nPreprocessing completed successfully!")

print("\nProcessed train shape:",
      X_train_processed.shape)

print("Processed test shape:",
      X_test_processed.shape)

print("\nTarget distribution:")
print(y.value_counts())

print("\nSaved files:")
print("data/processed/X_train.csv")
print("data/processed/X_test.csv")
print("data/processed/y_train.csv")
print("data/processed/y_test.csv")
print("models/ml/preprocessor.joblib")