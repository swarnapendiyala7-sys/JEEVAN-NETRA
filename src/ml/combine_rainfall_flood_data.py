import pandas as pd
import os

RAINFALL_FILE = "data/processed/regional_rainfall_risk.csv"
FLOOD_FILE = "data/processed/flood_impact_features.csv"
OUTPUT_FILE = "data/processed/combined_rainfall_flood_risk.csv"

# --------------------------------------------------
# 1. Load datasets
# --------------------------------------------------

rainfall = pd.read_csv(RAINFALL_FILE)
flood = pd.read_csv(FLOOD_FILE)

# --------------------------------------------------
# 2. Create state-level rainfall approximation
# --------------------------------------------------
# IMD has meteorological subdivisions, while the flood
# inventory uses states. Therefore, we aggregate rainfall
# subdivisions into state-level yearly values.
#
# This is an approximation, not a ground-truth flood label.

state_to_subdivision = {
    "Andhra Pradesh": [
        "Coastal Andhra Pradesh",
        "Rayalseema"
    ],
    "Telangana": [
        "Telangana"
    ],
    "Karnataka": [
        "Coastal Karnataka",
        "North Interior Karnataka",
        "South Interior Karnataka"
    ],
    "Kerala": [
        "Kerala"
    ],
    "Tamil Nadu": [
        "Tamil Nadu"
    ],
    "Odisha": [
        "Orissa"
    ],
    "West Bengal": [
        "Gangetic West Bengal",
        "Sub Himalayan West Bengal & Sikkim"
    ],
    "Assam": [
        "Assam & Meghalaya"
    ],
    "Bihar": [
        "Bihar"
    ],
    "Jharkhand": [
        "Jharkhand"
    ],
    "Uttar Pradesh": [
        "East Uttar Pradesh",
        "West Uttar Pradesh"
    ],
    "Rajasthan": [
        "East Rajasthan",
        "West Rajasthan"
    ],
    "Gujarat": [
        "Gujarat Region",
        "Saurashtra & Kutch"
    ],
    "Madhya Pradesh": [
        "West Madhya Pradesh",
        "East Madhya Pradesh"
    ],
    "Maharashtra": [
        "Madhya Maharashtra",
        "Marathwada",
        "Vidarbha"
    ],
    "Punjab": [
        "Punjab"
    ],
    "Haryana": [
        "Haryana, Chandigarh & Delhi"
    ],
    "Himachal Pradesh": [
        "Himachal Pradesh"
    ],
    "Uttarakhand": [
        "Uttarakhand"
    ],
    "Goa": [
        "Konkan & Goa"
    ],
    "Chhattisgarh": [
        "Chhattisgarh"
    ],
    "Arunachal Pradesh": [
        "Arunachal Pradesh"
    ],
    "Nagaland": [
        "Naga Mani Mizo Tripura"
    ],
    "Manipur": [
        "Naga Mani Mizo Tripura"
    ],
    "Mizoram": [
        "Naga Mani Mizo Tripura"
    ],
    "Tripura": [
        "Naga Mani Mizo Tripura"
    ],
    "Meghalaya": [
        "Assam & Meghalaya"
    ],
    "Sikkim": [
        "Sub Himalayan West Bengal & Sikkim"
    ],
    "Jammu and Kashmir": [
        "Jammu & Kashmir"
    ]
}

# Reverse mapping
subdivision_to_state = {}

for state, subdivisions in state_to_subdivision.items():
    for subdivision in subdivisions:
        subdivision_to_state[subdivision] = state

rainfall["State"] = rainfall["SUBDIVISION"].map(
    subdivision_to_state
)

# Remove subdivisions that could not be mapped
rainfall_mapped = rainfall.dropna(subset=["State"]).copy()

# --------------------------------------------------
# 3. Aggregate rainfall by State + Year
# --------------------------------------------------

rainfall_state_year = (
    rainfall_mapped
    .groupby(["State", "YEAR"], as_index=False)
    .agg(
        Annual_Rainfall=("ANNUAL", "mean"),
        Historical_Avg_Rainfall=("Historical_Avg_Rainfall", "mean"),
        Rainfall_Anomaly=("Rainfall_Anomaly", "mean"),
        Rainfall_Anomaly_Percent=("Rainfall_Anomaly_Percent", "mean"),
        Rainfall_Risk_Score=("Rainfall_Risk_Score", "mean")
    )
)

# Convert average rainfall risk score into categories
def rainfall_risk(score):
    if score >= 2.5:
        return "Critical"
    elif score >= 1.5:
        return "High"
    elif score >= 0.5:
        return "Moderate"
    else:
        return "Low"


rainfall_state_year["Regional_Rainfall_Risk"] = (
    rainfall_state_year["Rainfall_Risk_Score"]
    .apply(rainfall_risk)
)

# --------------------------------------------------
# 4. Aggregate historical flood impact by State + Year
# --------------------------------------------------

flood["Start Date"] = pd.to_datetime(
    flood["Start Date"],
    errors="coerce"
)

flood["Year"] = flood["Start Date"].dt.year

flood_state_year = (
    flood
    .groupby(["State", "Year"], as_index=False)
    .agg(
        Flood_Events=("UEI", "count"),
        Total_Known_Fatalities=("Human fatality", "sum"),
        Total_Known_Injuries=("Human injured", "sum"),
        Total_Known_Displaced=("Human Displaced", "sum"),
        Total_Animal_Fatalities=("Animal Fatality", "sum"),
        Average_Impact_Score=("Historical_Impact_Score", "mean")
    )
)

# --------------------------------------------------
# 5. Rename rainfall year
# --------------------------------------------------

rainfall_state_year = rainfall_state_year.rename(
    columns={"YEAR": "Year"}
)

# --------------------------------------------------
# 6. Combine rainfall + historical flood information
# --------------------------------------------------

combined = pd.merge(
    rainfall_state_year,
    flood_state_year,
    on=["State", "Year"],
    how="outer"
)

# --------------------------------------------------
# 7. Add simple combined risk signal
# --------------------------------------------------

combined["Flood_Events"] = combined["Flood_Events"].fillna(0)

combined["Total_Known_Fatalities"] = (
    combined["Total_Known_Fatalities"].fillna(0)
)

combined["Total_Known_Injuries"] = (
    combined["Total_Known_Injuries"].fillna(0)
)

combined["Total_Known_Displaced"] = (
    combined["Total_Known_Displaced"].fillna(0)
)

combined["Total_Animal_Fatalities"] = (
    combined["Total_Animal_Fatalities"].fillna(0)
)

# Historical flood presence
combined["Historical_Flood_Present"] = (
    combined["Flood_Events"] > 0
).astype(int)

# Combined signal:
# rainfall score + historical flood presence
combined["Combined_Risk_Score"] = (
    combined["Rainfall_Risk_Score"].fillna(0)
    + combined["Historical_Flood_Present"]
)

# --------------------------------------------------
# 8. Classify combined risk
# --------------------------------------------------

def combined_risk(score):

    if score >= 3:
        return "Critical"
    elif score >= 2:
        return "High"
    elif score >= 1:
        return "Moderate"
    else:
        return "Low"


combined["Combined_Risk_Level"] = (
    combined["Combined_Risk_Score"]
    .apply(combined_risk)
)

# --------------------------------------------------
# 9. Save
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

combined.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# 10. Summary
# --------------------------------------------------

print("Rainfall + Flood data combination completed!")

print(f"\nRows: {len(combined)}")
print(f"Columns: {len(combined.columns)}")

print("\nCombined Risk Distribution:")
print(
    combined["Combined_Risk_Level"]
    .value_counts()
)

print("\nTop States by Historical Flood Events:")

print(
    flood_state_year
    .groupby("State")["Flood_Events"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

print(f"\nSaved to: {OUTPUT_FILE}")