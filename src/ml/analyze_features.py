import pandas as pd

# Load original dataset
df = pd.read_csv("data/raw/flood_risk_dataset_india.csv")

target = "Flood Occurred"

print("========== DATASET ANALYSIS ==========\n")

# Target distribution
print("Target Distribution:")
print(df[target].value_counts())

print("\nTarget Percentage:")
print(df[target].value_counts(normalize=True) * 100)

# Numerical feature correlations
numeric_columns = df.select_dtypes(include="number").columns

correlations = (
    df[numeric_columns]
    .corr()[target]
    .drop(target)
    .sort_values(key=abs, ascending=False)
)

print("\n========== NUMERICAL FEATURE CORRELATION ==========\n")
print(correlations)

# Average values for each target class
print("\n========== FEATURE AVERAGES BY FLOOD STATUS ==========\n")

numeric_features = [
    "Latitude",
    "Longitude",
    "Rainfall (mm)",
    "Temperature (°C)",
    "Humidity (%)",
    "River Discharge (m³/s)",
    "Water Level (m)",
    "Elevation (m)",
    "Population Density",
    "Infrastructure",
    "Historical Floods"
]

print(
    df.groupby(target)[numeric_features]
    .mean()
    .round(2)
)

# Categorical relationship
print("\n========== LAND COVER vs FLOOD ==========\n")

print(
    pd.crosstab(
        df["Land Cover"],
        df[target],
        normalize="index"
    ).round(3)
)

print("\n========== SOIL TYPE vs FLOOD ==========\n")

print(
    pd.crosstab(
        df["Soil Type"],
        df[target],
        normalize="index"
    ).round(3)
)

print("\n========== ANALYSIS COMPLETED ==========")