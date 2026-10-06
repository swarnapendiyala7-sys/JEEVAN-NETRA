import geopandas as gpd
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

OUTPUT_FILE = BASE_DIR / "vijayawada_risk_roads.geojson"


# ============================================================
# STEP 1: CONVERT RISK RASTER TO POLYGONS
# ============================================================

print("\nReading satellite-derived risk zones...")

with rasterio.open(RISK_RASTER) as src:

    risk_data = src.read(1)
    transform = src.transform
    raster_crs = src.crs

    # Risk zone pixels = 1
    mask = risk_data > 0

    polygon_list = []

    for geom, value in shapes(
        risk_data,
        mask=mask,
        transform=transform
    ):
        if value > 0:
            polygon_list.append(shape(geom))


print(f"Risk-zone polygons created: {len(polygon_list)}")


# ============================================================
# STEP 2: CREATE RISK-ZONE GEODATAFRAME
# ============================================================

risk_gdf = gpd.GeoDataFrame(
    {"risk_zone": [1] * len(polygon_list)},
    geometry=polygon_list,
    crs=raster_crs
)


# ============================================================
# STEP 3: READ OSM ROADS
# ============================================================

print("\nReading OSM road network...")

roads = gpd.read_file(ROADS_FILE)

print(f"Road segments loaded: {len(roads)}")
print(f"Road CRS: {roads.crs}")


# ============================================================
# STEP 4: MATCH CRS
# ============================================================

if roads.crs != risk_gdf.crs:
    roads = roads.to_crs(risk_gdf.crs)


# ============================================================
# STEP 5: FIND ROADS INTERSECTING RISK ZONES
# ============================================================

print("\nFinding roads intersecting satellite risk zones...")

risk_union = risk_gdf.geometry.union_all()

roads["risk_intersection"] = roads.geometry.intersects(risk_union)

affected_roads = roads[
    roads["risk_intersection"] == True
].copy()


# ============================================================
# STEP 6: SUMMARY
# ============================================================

print("\n===================================")
print("ROAD RISK INTERSECTION")
print("===================================")

print(f"Total road segments: {len(roads)}")
print(f"Potentially affected roads: {len(affected_roads)}")


if len(roads) > 0:

    percentage = (
        len(affected_roads) / len(roads)
    ) * 100

    print(
        f"Potentially affected percentage: "
        f"{percentage:.2f}%"
    )


# ============================================================
# STEP 7: ROAD TYPE SUMMARY
# ============================================================

if len(affected_roads) > 0:

    print("\nPotentially affected road types:")

    print(
        affected_roads["highway"]
        .value_counts()
    )


# ============================================================
# STEP 8: SAVE RESULT
# ============================================================

affected_roads.to_file(
    OUTPUT_FILE,
    driver="GeoJSON"
)

print("\nSaved:")
print(OUTPUT_FILE)

print(
    "\nIMPORTANT:"
    "\nThese are roads intersecting satellite-derived "
    "high-risk evidence zones."
    "\nThey are NOT confirmed flooded roads."
)