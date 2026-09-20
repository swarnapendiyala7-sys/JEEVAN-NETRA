import pandas as pd
import os
import re

INPUT_FILE = "data/raw/India_Flood_Inventory_v3.csv"
OUTPUT_FILE = "data/processed/flood_inventory_clean.csv"

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# 1. Remove unnecessary column
# --------------------------------------------------

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])


# --------------------------------------------------
# 2. Convert dates correctly
# --------------------------------------------------

df["Start Date"] = pd.to_datetime(
    df["Start Date"],
    dayfirst=True,
    errors="coerce"
)

df["End Date"] = pd.to_datetime(
    df["End Date"],
    dayfirst=True,
    errors="coerce"
)

# Create useful time features
df["Year"] = df["Start Date"].dt.year
df["Month"] = df["Start Date"].dt.month


# --------------------------------------------------
# 3. Clean State names
# --------------------------------------------------

df["State"] = (
    df["State"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Standardize Jammu & Kashmir naming
df["State"] = df["State"].replace({
    "Jammu & Kashmir": "Jammu and Kashmir"
})


# --------------------------------------------------
# 4. Clean Main Cause
# --------------------------------------------------

def clean_cause(value):

    if pd.isna(value):
        return "Unknown"

    value = str(value).strip().lower()

    if "landslide" in value:
        return "Landslide"

    if "flash flood" in value:
        return "Flash Flood"

    if "heavy rain" in value:
        return "Heavy Rain"

    if "flood" in value:
        return "Flood"

    if "cyclone" in value:
        return "Cyclone"

    if "cloudburst" in value:
        return "Cloudburst"

    if "dam" in value:
        return "Dam/Reservoir"

    if "river" in value:
        return "River Flood"

    if "snow" in value:
        return "Snow/Glacier"

    if "severe" in value:
        return "Severe Weather"

    return "Other"


df["Main_Cause_Clean"] = df["Main Cause"].apply(clean_cause)


# --------------------------------------------------
# 5. Convert impact columns to numeric
# --------------------------------------------------

impact_columns = [
    "Human fatality",
    "Human injured",
    "Human Displaced",
    "Animal Fatality"
]

for column in impact_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# 6. Create availability indicators
# --------------------------------------------------

for column in impact_columns:
    indicator_name = column.replace(" ", "_") + "_Available"

    df[indicator_name] = df[column].notna().astype(int)


# --------------------------------------------------
# 7. Create total known human impact
# --------------------------------------------------

df["Known_Human_Impact"] = (
    df["Human fatality"].fillna(0)
    + df["Human injured"].fillna(0)
    + df["Human Displaced"].fillna(0)
)


# --------------------------------------------------
# 8. Create flood event duration if necessary
# --------------------------------------------------

df["Calculated_Duration_Days"] = (
    df["End Date"] - df["Start Date"]
).dt.days + 1


# --------------------------------------------------
# 9. Save cleaned dataset
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 10. Print summary
# --------------------------------------------------

print("Flood inventory cleaning completed!")

print(f"\nRows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nDate range:")
print(df["Year"].min(), "to", df["Year"].max())

print("\nTop States:")
print(df["State"].value_counts().head(15))

print("\nCleaned Main Causes:")
print(df["Main_Cause_Clean"].value_counts())

print(f"\nSaved to: {OUTPUT_FILE}")