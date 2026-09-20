import pandas as pd

df = pd.read_csv("data/raw/flood_risk_dataset_india.csv")

target = "Flood Occurred"

print("========== TARGET INSPECTION ==========\n")

print("Target values:")
print(df[target].unique())

print("\nTarget counts:")
print(df[target].value_counts())

print("\nAverage feature values by target:")
print(
    df.groupby(target).mean(numeric_only=True).round(2)
)

print("\nRainfall by target:")
print(
    df.groupby(target)["Rainfall (mm)"]
    .agg(["min", "mean", "max"])
    .round(2)
)

print("\nRiver Discharge by target:")
print(
    df.groupby(target)["River Discharge (m³/s)"]
    .agg(["min", "mean", "max"])
    .round(2)
)

print("\nWater Level by target:")
print(
    df.groupby(target)["Water Level (m)"]
    .agg(["min", "mean", "max"])
    .round(2)
)

print("\nHistorical Floods by target:")
print(
    df.groupby(target)["Historical Floods"]
    .agg(["min", "mean", "max"])
    .round(2)
)

print("\n========== INSPECTION COMPLETED ==========")