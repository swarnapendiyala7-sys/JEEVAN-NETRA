import pandas as pd
import os

INPUT_FILE = "data/processed/rainfall_risk_features.csv"
OUTPUT_FILE = "data/processed/regional_rainfall_risk.csv"

df = pd.read_csv(INPUT_FILE)

# Convert rainfall stress into a numerical risk score
risk_scores = {
    "Normal": 0,
    "Elevated": 1,
    "High": 2,
    "Extreme": 3
}

df["Rainfall_Risk_Score"] = df["Rainfall_Stress_Level"].map(risk_scores)

# Create a simple regional risk signal
def classify_risk(score):
    if score == 3:
        return "Critical"
    elif score == 2:
        return "High"
    elif score == 1:
        return "Moderate"
    else:
        return "Low"


df["Regional_Rainfall_Risk"] = df["Rainfall_Risk_Score"].apply(
    classify_risk
)

# Save final rainfall risk dataset
os.makedirs("data/processed", exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("Regional rainfall risk model completed!")
print(f"Rows: {len(df)}")

print("\nRegional Rainfall Risk Distribution:")
print(df["Regional_Rainfall_Risk"].value_counts())

print(f"\nSaved to: {OUTPUT_FILE}")