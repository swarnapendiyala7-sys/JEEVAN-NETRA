import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RISK_RASTER = BASE_DIR / "vijayawada_risk_zones.tiff"
ROADS_FILE = BASE_DIR / "vijayawada_roads.geojson"
AFFECTED_ROADS_FILE = BASE_DIR / "vijayawada_risk_roads.geojson"

OUTPUT_IMAGE = BASE_DIR / "vijayawada_road_risk_map.png"


# ============================================================
# STEP 1: READ RISK ZONES
# ============================================================

print("\nReading satellite risk zones...")

with rasterio.open(RISK_RASTER) as src:

    risk_data = src.read(1)
    transform = src.transform
    raster_crs = src.crs

    mask = risk_data > 0

    polygons = []

    for geom, value in shapes(
        risk_data,
        mask=mask,
        transform=transform
    ):
        if value > 0:
            polygons.append(shape(geom))


risk_gdf = gpd.GeoDataFrame(
    {"risk_zone": [1] * len(polygons)},
    geometry=polygons,
    crs=raster_crs
)

print(f"Risk polygons: {len(risk_gdf)}")


# ============================================================
# STEP 2: READ ALL ROADS
# ============================================================

print("Reading all roads...")

roads = gpd.read_file(ROADS_FILE)

if roads.crs != raster_crs:
    roads = roads.to_crs(raster_crs)

print(f"Total roads: {len(roads)}")


# ============================================================
# STEP 3: READ AFFECTED ROADS
# ============================================================

print("Reading potentially affected roads...")

affected_roads = gpd.read_file(AFFECTED_ROADS_FILE)

if affected_roads.crs != raster_crs:
    affected_roads = affected_roads.to_crs(raster_crs)

print(f"Potentially affected roads: {len(affected_roads)}")


# ============================================================
# STEP 4: CREATE MAP
# ============================================================

print("\nCreating road-risk map...")

fig, ax = plt.subplots(figsize=(12, 10))


# All roads
roads.plot(
    ax=ax,
    linewidth=0.25,
    alpha=0.35
)


# Satellite risk zones
risk_gdf.plot(
    ax=ax,
    alpha=0.35
)


# Potentially affected roads
affected_roads.plot(
    ax=ax,
    linewidth=1.2
)


# ============================================================
# STEP 5: TITLE
# ============================================================

ax.set_title(
    "JEEVAN-NETRA 2.0\n"
    "Satellite-Derived Risk Zones & Potentially Affected Roads",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")


# ============================================================
# STEP 6: GRID
# ============================================================

ax.grid(
    True,
    alpha=0.2
)


# ============================================================
# STEP 7: SAVE
# ============================================================

plt.tight_layout()

plt.savefig(
    OUTPUT_IMAGE,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


print("\n===================================")
print("ROAD RISK MAP CREATED")
print("===================================")

print("Saved:")
print(OUTPUT_IMAGE)

print("\nMap contains:")
print("1. OSM road network")
print("2. Satellite-derived risk zones")
print("3. Potentially affected road segments")