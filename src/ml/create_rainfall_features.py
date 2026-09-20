import pandas as pd
import os

INPUT_FILE = "data/processed/imd_rainfall_clean.csv"
OUTPUT_FILE = "data/processed/rainfall_features.csv"

df = pd.read_csv(INPUT_FILE)

# Historical average rainfall for each subdivision
historical_avg = df.groupby("SUBDIVISION")["ANNUAL"].mean()

# Add historical average
df["Historical_Avg_Rainfall"] = df["SUBDIVISION"].map(historical_avg)

# Calculate rainfall anomaly
df["Rainfall_Anomaly"] = (
    df["ANNUAL"] - df["Historical_Avg_Rainfall"]
)

# Calculate percentage anomaly
df["Rainfall_Anomaly_Percent"] = (
    df["Rainfall_Anomaly"]
    / df["Historical_Avg_Rainfall"]
) * 100

# Save
os.makedirs("data/processed", exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Rainfall feature engineering completed!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {OUTPUT_FILE}")