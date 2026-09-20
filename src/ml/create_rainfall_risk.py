import pandas as pd
import os

INPUT_FILE = "data/processed/rainfall_features.csv"
OUTPUT_FILE = "data/processed/rainfall_risk_features.csv"

df = pd.read_csv(INPUT_FILE)

# Data-driven rainfall anomaly categories.
# These describe rainfall stress, NOT actual flood occurrence.
def classify_rainfall(anomaly):
    if anomaly >= 55:
        return "Extreme"
    elif anomaly >= 34:
        return "High"
    elif anomaly >= 12:
        return "Elevated"
    else:
        return "Normal"


# Create rainfall stress category
df["Rainfall_Stress_Level"] = df["Rainfall_Anomaly_Percent"].apply(
    classify_rainfall
)

# Save processed dataset
os.makedirs("data/processed", exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Rainfall risk feature creation completed!")
print(f"Rows: {len(df)}")
print("\nRainfall Stress Distribution:")
print(df["Rainfall_Stress_Level"].value_counts())

print(f"\nSaved to: {OUTPUT_FILE}")