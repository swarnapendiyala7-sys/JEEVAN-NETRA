import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "ml" / "historical_flood_model.joblib"
PREPROCESSOR_PATH = BASE_DIR / "models" / "ml" / "historical_flood_preprocessor.joblib"


# ============================================================
# 2. LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

print("Historical Flood Model loaded successfully!")


# ============================================================
# 3. TEST INPUT
# ============================================================

state = input("Enter State: ")

year = int(input("Enter Year: "))

annual_rainfall = float(
    input("Enter Annual Rainfall (mm): ")
)

historical_avg_rainfall = float(
    input("Enter Historical Average Rainfall (mm): ")
)

rainfall_anomaly = float(
    input("Enter Rainfall Anomaly (mm): ")
)

rainfall_anomaly_percent = float(
    input("Enter Rainfall Anomaly (%): ")
)

rainfall_risk_score = int(
    input("Enter Rainfall Risk Score (0-3): ")
)


# ============================================================
# 4. CREATE INPUT DATAFRAME
# ============================================================

input_data = pd.DataFrame([{
    "State": state,
    "Year": year,
    "Annual_Rainfall": annual_rainfall,
    "Historical_Avg_Rainfall": historical_avg_rainfall,
    "Rainfall_Anomaly": rainfall_anomaly,
    "Rainfall_Anomaly_Percent": rainfall_anomaly_percent,
    "Rainfall_Risk_Score": rainfall_risk_score
}])


# ============================================================
# 5. PREPROCESS INPUT
# ============================================================

input_processed = preprocessor.transform(input_data)


# ============================================================
# 6. PREDICTION
# ============================================================

prediction = model.predict(input_processed)[0]

probability = model.predict_proba(input_processed)[0]

flood_probability = probability[1] * 100


# ============================================================
# 7. RISK LEVEL
# ============================================================

if flood_probability >= 75:
    risk_level = "CRITICAL"

elif flood_probability >= 50:
    risk_level = "HIGH"

elif flood_probability >= 25:
    risk_level = "MODERATE"

else:
    risk_level = "LOW"


# ============================================================
# 8. RESULT
# ============================================================

print("\n========================================")
print("      JEEVAN-NETRA FLOOD PREDICTION")
print("========================================")

if prediction == 1:
    print("Prediction       : FLOOD")
else:
    print("Prediction       : NO FLOOD")

print(f"Flood Probability: {flood_probability:.2f}%")
print(f"Risk Level       : {risk_level}")

print("========================================")