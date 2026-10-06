import geopandas as gpd
import rasterio
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ROADS_FILE = BASE_DIR / "vijayawada_risk_roads.geojson"
RISK_RASTER = BASE_DIR / "vijayawada_multimodal_risk_smooth.tiff"

OUTPUT_FILE = BASE_DIR / "vijayawada_road_risk_scored.geojson"


# ============================================================
# LOAD ROADS
# ============================================================

print("\nLoading potentially affected roads...")

roads = gpd.read_file(ROADS_FILE)

print(f"Roads loaded: {len(roads)}")


# ============================================================
# LOAD RISK RASTER
# ============================================================

print("\nLoading multi-modal risk raster...")

with rasterio.open(RISK_RASTER) as src:

    risk = src.read(1)

    transform = src.transform
    raster_crs = src.crs
    bounds = src.bounds

print(f"Raster shape: {risk.shape}")
print(f"Raster CRS: {raster_crs}")


# ============================================================
# CRS MATCH
# ============================================================

if roads.crs != raster_crs:
    roads = roads.to_crs(raster_crs)


# ============================================================
# RISK SCORE EXTRACTION
# ============================================================

print("\nCalculating road-level risk scores...")


def calculate_road_score(geometry):

    # Find pixels touched by the road bounding box
    minx, miny, maxx, maxy = geometry.bounds

    row_min, col_min = rasterio.transform.rowcol(
        transform,
        minx,
        maxy
    )

    row_max, col_max = rasterio.transform.rowcol(
        transform,
        maxx,
        miny
    )

    row_start = max(0, min(row_min, row_max))
    row_end = min(risk.shape[0], max(row_min, row_max) + 1)

    col_start = max(0, min(col_min, col_max))
    col_end = min(risk.shape[1], max(col_min, col_max) + 1)

    if row_start >= row_end or col_start >= col_end:
        return np.nan

    values = risk[
        row_start:row_end,
        col_start:col_end
    ]

    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.nan

    return float(np.mean(values))


roads["risk_score"] = roads.geometry.apply(
    calculate_road_score
)


# ============================================================
# NORMALIZE SCORE
# ============================================================

valid_scores = roads["risk_score"].dropna()

if len(valid_scores) > 0:

    min_score = valid_scores.min()
    max_score = valid_scores.max()

    if max_score > min_score:

        roads["normalized_risk"] = (
            (roads["risk_score"] - min_score)
            / (max_score - min_score)
        ) * 100

    else:

        roads["normalized_risk"] = 0

else:

    roads["normalized_risk"] = np.nan


# ============================================================
# RISK LEVEL
# ============================================================

def classify_risk(score):

    if np.isnan(score):
        return "UNKNOWN"

    if score >= 75:
        return "CRITICAL"

    if score >= 50:
        return "HIGH"

    if score >= 25:
        return "MEDIUM"

    return "LOW"


roads["risk_level"] = roads["normalized_risk"].apply(
    classify_risk
)


# ============================================================
# SORT
# ============================================================

roads = roads.sort_values(
    "normalized_risk",
    ascending=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n===================================")
print("ROAD-LEVEL RISK ANALYSIS")
print("===================================")

print(f"Total roads: {len(roads)}")

print("\nRisk levels:")

print(
    roads["risk_level"]
    .value_counts()
)


print("\nTop 10 potentially affected roads:")

columns = [
    "name",
    "highway",
    "normalized_risk",
    "risk_level"
]

available_columns = [
    c for c in columns
    if c in roads.columns
]

print(
    roads[available_columns]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# SAVE
# ============================================================

roads.to_file(
    OUTPUT_FILE,
    driver="GeoJSON"
)

print("\n===================================")
print("ROAD RISK DATA SAVED")
print("===================================")

print(OUTPUT_FILE)

print(
    "\nNOTE:"
    "\nRisk levels represent satellite-derived "
    "multi-modal evidence associated with roads."
    "\nThey are not confirmed flood predictions."
)