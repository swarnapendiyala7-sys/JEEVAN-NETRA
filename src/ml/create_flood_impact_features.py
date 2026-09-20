import pandas as pd
import os

INPUT_FILE = "data/processed/flood_inventory_clean.csv"
OUTPUT_FILE = "data/processed/flood_impact_features.csv"

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# 1. Convert impact columns to numeric
# --------------------------------------------------

impact_columns = [
    "Human fatality",
    "Human injured",
    "Human Displaced",
    "Animal Fatality"
]

for column in impact_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# --------------------------------------------------
# 2. Create impact indicators
# --------------------------------------------------

df["Fatality_Reported"] = df["Human fatality"].notna().astype(int)
df["Injury_Reported"] = df["Human injured"].notna().astype(int)
df["Displacement_Reported"] = df["Human Displaced"].notna().astype(int)
df["Animal_Impact_Reported"] = df["Animal Fatality"].notna().astype(int)


# --------------------------------------------------
# 3. Create known human impact
# Missing values are NOT treated as zero here.
# --------------------------------------------------

df["Known_Human_Impact"] = (
    df["Human fatality"].fillna(0)
    + df["Human injured"].fillna(0)
    + df["Human Displaced"].fillna(0)
)


# --------------------------------------------------
# 4. Create impact severity signal
# This is based only on reported fatalities.
# It is NOT a ground-truth severity label.
# --------------------------------------------------

def classify_impact(row):

    fatalities = row["Human fatality"]

    if pd.isna(fatalities):
        return "Unknown"

    if fatalities >= 100:
        return "Extreme"
    elif fatalities >= 25:
        return "High"
    elif fatalities >= 5:
        return "Moderate"
    elif fatalities > 0:
        return "Low"
    else:
        return "No Fatality Reported"


df["Historical_Impact_Level"] = df.apply(
    classify_impact,
    axis=1
)


# --------------------------------------------------
# 5. Create event-level risk signal
# --------------------------------------------------

impact_score = {
    "No Fatality Reported": 0,
    "Low": 1,
    "Moderate": 2,
    "High": 3,
    "Extreme": 4,
    "Unknown": -1
}

df["Historical_Impact_Score"] = (
    df["Historical_Impact_Level"].map(impact_score)
)


# --------------------------------------------------
# 6. Save
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 7. Summary
# --------------------------------------------------

print("Flood impact feature creation completed!")

print(f"\nRows: {len(df)}")

print("\nHistorical Impact Level:")
print(
    df["Historical_Impact_Level"]
    .value_counts()
)

print("\nImpact Score:")
print(
    df["Historical_Impact_Score"]
    .value_counts()
    .sort_index()
)

print(f"\nSaved to: {OUTPUT_FILE}")