import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# =========================
# 1. Paths
# =========================

MODEL_PATH = "models/ml/flood_risk_model.joblib"

X_TEST_PATH = "data/processed/X_test.csv"
Y_TEST_PATH = "data/processed/y_test.csv"


# =========================
# 2. Load model and test data
# =========================

print("Loading model...")

model = joblib.load(MODEL_PATH)

X_test = pd.read_csv(X_TEST_PATH)
y_test = pd.read_csv(Y_TEST_PATH).squeeze()

print("X_test:", X_test.shape)
print("y_test:", y_test.shape)


# =========================
# 3. Make predictions
# =========================

print("\nMaking predictions...")

y_pred = model.predict(X_test)


# =========================
# 4. Calculate metrics
# =========================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)


# =========================
# 5. Display results
# =========================

print("\n========== MODEL EVALUATION ==========")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")


# =========================
# 6. Confusion Matrix
# =========================

print("\nConfusion Matrix:")

cm = confusion_matrix(y_test, y_pred)

print(cm)


# =========================
# 7. Classification Report
# =========================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["No Flood", "Flood"]
    )
)


# =========================
# 8. Save evaluation results
# =========================

results = {
    "Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1 Score": f1
}

results_df = pd.DataFrame([results])

results_df.to_csv(
    "models/ml/evaluation_results.csv",
    index=False
)

print("\nEvaluation results saved to:")
print("models/ml/evaluation_results.csv")

print("\nModel evaluation completed successfully!")