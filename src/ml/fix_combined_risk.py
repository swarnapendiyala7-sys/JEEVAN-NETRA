import pandas as pd
import os

INPUT_FILE = "data/processed/combined_rainfall_flood_risk.csv"
OUTPUT_FILE = "data/processed/final_historical_risk.csv"

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# 1. Check whether rainfall information is available
# --------------------------------------------------

df["Rainfall_Data_Available"] = (
    df["Annual_Rainfall"].notna()
).astype(int)


# --------------------------------------------------
# 2. Improve combined risk classification
# --------------------------------------------------

def classify_final_risk(row):

    rainfall_available = row["Rainfall_Data_Available"]
    flood_events = row["Flood_Events"]
    rainfall_score = row["Rainfall_Risk_Score"]

    # No rainfall information and no historical flood
    if rainfall_available == 0 and flood_events == 0:
        return "Insufficient Data"

    # Rainfall unavailable but historical flood exists
    if rainfall_available == 0 and flood_events > 0:
        return "Historical Flood Signal"

    # Rainfall is available
    score = rainfall_score

    if flood_events > 0:
        score += 1

    if score >= 3:
        return "Critical"
    elif score >= 2:
        return "High"
    elif score >= 1:
        return "Moderate"
    else:
        return "Low"


df["Final_Risk_Level"] = df.apply(
    classify_final_risk,
    axis=1
)


# --------------------------------------------------
# 3. Create a clear numeric risk score
# --------------------------------------------------

risk_score_map = {
    "Low": 0,
    "Moderate": 1,
    "High": 2,
    "Critical": 3,
    "Historical Flood Signal": 2,
    "Insufficient Data": -1
}

df["Final_Risk_Score"] = (
    df["Final_Risk_Level"].map(risk_score_map)
)


# --------------------------------------------------
# 4. Save
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 5. Summary
# --------------------------------------------------

print("Final historical risk dataset created!")

print(f"\nRows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nFinal Risk Distribution:")
print(
    df["Final_Risk_Level"]
    .value_counts()
)

print("\nRainfall Data Availability:")
print(
    df["Rainfall_Data_Available"]
    .value_counts()
)

print(f"\nSaved to: {OUTPUT_FILE}")