import numpy as np
import pandas as pd
import rasterio


# ============================================================
# JEEVAN-NETRA 2.0
# Sentinel-1 Radar + Historical Rainfall Context
# ============================================================

RADAR_FILE = "vijayawada_radar_change_score.tiff"
RAINFALL_FILE = "data/processed/rainfall_risk_features.csv"

OUTPUT_FILE = "vijayawada_multimodal_risk.tiff"


# ------------------------------------------------------------
# 1. Read Sentinel-1 radar score
# ------------------------------------------------------------

print("Reading Sentinel-1 radar change score...")

with rasterio.open(RADAR_FILE) as src:
    radar = src.read(1).astype(np.float32)
    profile = src.profile.copy()

print("Radar shape:", radar.shape)
print("Radar CRS:", profile["crs"])


# ------------------------------------------------------------
# 2. Read historical rainfall dataset
# ------------------------------------------------------------

print()
print("Reading historical rainfall data...")

df = pd.read_csv(RAINFALL_FILE)

# Vijayawada is in the Coastal Andhra region.
ap = df[
    df["SUBDIVISION"]
    .astype(str)
    .str.contains("Coastal Andhra Pradesh", case=False, na=False)
].copy()

if ap.empty:
    raise ValueError(
        "Coastal Andhra Pradesh rainfall records not found."
    )

print("Coastal Andhra records:", len(ap))


# ------------------------------------------------------------
# 3. Select latest available historical year
# ------------------------------------------------------------

ap = ap.sort_values("YEAR")

latest = ap.iloc[-1]

year = int(latest["YEAR"])
annual = float(latest["ANNUAL"])
historical_avg = float(
    latest["Historical_Avg_Rainfall"]
)
anomaly_percent = float(
    latest["Rainfall_Anomaly_Percent"]
)
stress_level = str(
    latest["Rainfall_Stress_Level"]
)

print()
print("Historical rainfall context")
print("---------------------------")
print("Year:", year)
print("Annual rainfall:", annual)
print("Historical average:", historical_avg)
print(
    "Rainfall anomaly %:",
    round(anomaly_percent, 2)
)
print("Stress level:", stress_level)


# ------------------------------------------------------------
# 4. Convert rainfall anomaly into evidence score
# ------------------------------------------------------------

# Historical anomaly is used only as regional context.
#
# Negative anomaly -> low evidence
# Near-normal     -> moderate baseline
# Positive anomaly -> increasing evidence
#
# We cap the value to avoid extreme historical
# values dominating the satellite signal.

rainfall_evidence = np.clip(
    50 + anomaly_percent,
    0,
    100
)

print(
    "Historical rainfall evidence:",
    round(float(rainfall_evidence), 2)
)


# ------------------------------------------------------------
# 5. Normalize radar score
# ------------------------------------------------------------

valid = radar[np.isfinite(radar)]

radar_low = np.percentile(valid, 2)
radar_high = np.percentile(valid, 98)

if radar_high <= radar_low:
    raise ValueError(
        "Radar data does not contain enough variation."
    )

radar_normalized = (
    (radar - radar_low)
    / (radar_high - radar_low)
) * 100

radar_normalized = np.clip(
    radar_normalized,
    0,
    100
)


# ------------------------------------------------------------
# 6. Multi-modal evidence fusion
# ------------------------------------------------------------

RADAR_WEIGHT = 0.70
RAINFALL_WEIGHT = 0.30

multimodal_risk = (
    RADAR_WEIGHT * radar_normalized
    + RAINFALL_WEIGHT * rainfall_evidence
)

multimodal_risk = np.clip(
    multimodal_risk,
    0,
    100
).astype(np.float32)


# ------------------------------------------------------------
# 7. Save GeoTIFF
# ------------------------------------------------------------

profile.update(
    dtype="float32",
    count=1,
    compress="lzw"
)

with rasterio.open(
    OUTPUT_FILE,
    "w",
    **profile
) as dst:
    dst.write(multimodal_risk, 1)


# ------------------------------------------------------------
# 8. Final statistics
# ------------------------------------------------------------

print()
print("===================================")
print("MULTI-MODAL RISK FUSION")
print("===================================")

print(
    "Minimum:",
    round(float(np.nanmin(multimodal_risk)), 2)
)

print(
    "Maximum:",
    round(float(np.nanmax(multimodal_risk)), 2)
)

print(
    "Mean:",
    round(float(np.nanmean(multimodal_risk)), 2)
)

print(
    "Median:",
    round(float(np.nanmedian(multimodal_risk)), 2)
)

print()
print("Radar weight:", RADAR_WEIGHT)
print("Rainfall context weight:", RAINFALL_WEIGHT)

print()
print("Output:")
print(OUTPUT_FILE)

print()
print(
    "IMPORTANT: Rainfall is historical regional context."
)
print(
    "This layer is not a live rainfall measurement"
)
print(
    "and is not a confirmed flood probability."
)