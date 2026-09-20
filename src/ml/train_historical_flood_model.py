import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "processed" / "final_historical_risk.csv"
MODEL_DIR = BASE_DIR / "models" / "ml"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ============================================================
# 3. USE ONLY INFORMATION AVAILABLE BEFORE / DURING
#    THE FLOOD EVENT
# ============================================================

# Target
target = "Historical_Flood_Present"

# Features
features = [
    "State",
    "Year",
    "Annual_Rainfall",
    "Historical_Avg_Rainfall",
    "Rainfall_Anomaly",
    "Rainfall_Anomaly_Percent",
    "Rainfall_Risk_Score"
]

# Keep only required columns
data = df[features + [target]].copy()


# ============================================================
# 4. REMOVE ROWS WITH MISSING REQUIRED VALUES
# ============================================================

data = data.dropna()

print("\nClean dataset shape:", data.shape)


# ============================================================
# 5. CHECK TARGET
# ============================================================

print("\nTarget distribution:")
print(data[target].value_counts())


# ============================================================
# 6. SPLIT FEATURES AND TARGET
# ============================================================

X = data[features]
y = data[target].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape)
print("Testing samples :", X_test.shape)


# ============================================================
# 7. PREPROCESSING
# ============================================================

categorical_features = ["State"]

numeric_features = [
    "Year",
    "Annual_Rainfall",
    "Historical_Avg_Rainfall",
    "Rainfall_Anomaly",
    "Rainfall_Anomaly_Percent",
    "Rainfall_Risk_Score"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# ============================================================
# 8. TRANSFORM DATA
# ============================================================

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

print("\nProcessed training shape:", X_train_processed.shape)
print("Processed testing shape :", X_test_processed.shape)


# ============================================================
# 9. TRAIN RANDOM FOREST
# ============================================================

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train_processed, y_train)

print("\nModel training completed successfully!")


# ============================================================
# 10. PREDICTION
# ============================================================

y_pred = model.predict(X_test_processed)


# ============================================================
# 11. EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["No Flood", "Flood"],
    zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================================
# 12. SAVE MODEL
# ============================================================

model_path = MODEL_DIR / "historical_flood_model.joblib"
preprocessor_path = MODEL_DIR / "historical_flood_preprocessor.joblib"

joblib.dump(model, model_path)
joblib.dump(preprocessor, preprocessor_path)


# ============================================================
# 13. SAVE EVALUATION RESULTS
# ============================================================

evaluation = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ],
    "Score": [
        accuracy,
        precision,
        recall,
        f1
    ]
})

evaluation_path = MODEL_DIR / "historical_flood_evaluation.csv"
evaluation.to_csv(evaluation_path, index=False)


# ============================================================
# 14. FINAL OUTPUT
# ============================================================

print("\n==============================")
print("FILES SAVED")
print("==============================")

print("Model:")
print(model_path)

print("\nPreprocessor:")
print(preprocessor_path)

print("\nEvaluation:")
print(evaluation_path)

print("\nHistorical Flood Model is ready!")