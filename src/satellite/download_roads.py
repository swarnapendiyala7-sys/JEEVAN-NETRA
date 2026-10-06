import requests
import geopandas as gpd
from shapely.geometry import LineString


# ============================================================
# JEEVAN-NETRA 2.0
# OpenStreetMap Road Network Downloader
# ============================================================

BBOX = "16.45,80.55,16.60,80.75"

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

OUTPUT_FILE = "vijayawada_roads.geojson"

QUERY = f"""
[out:json][timeout:120];
way["highway"]({BBOX});
out geom;
"""


headers = {
    "User-Agent": "JEEVAN-NETRA/2.0 research project"
}


data = None

for url in OVERPASS_ENDPOINTS:

    print()
    print("Trying:", url)

    try:
        response = requests.post(
            url,
            data={"data": QUERY},
            headers=headers,
            timeout=180
        )

        print("HTTP Status:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("Successfully received OSM data.")
            break

        print("Server response:", response.text[:300])

    except requests.RequestException as e:
        print("Request failed:", e)


if data is None:
    raise RuntimeError(
        "Could not retrieve OpenStreetMap road data "
        "from the available Overpass endpoints."
    )


elements = data.get("elements", [])

print()
print("Road features received:", len(elements))


features = []

for element in elements:

    if element.get("type") != "way":
        continue

    geometry = element.get("geometry", [])

    if len(geometry) < 2:
        continue

    coordinates = [
        (point["lon"], point["lat"])
        for point in geometry
    ]

    try:
        line = LineString(coordinates)
    except Exception:
        continue

    tags = element.get("tags", {})

    features.append({
        "osm_id": element["id"],
        "name": tags.get("name", "Unnamed Road"),
        "highway": tags.get("highway", "unknown"),
        "geometry": line
    })


if not features:
    raise RuntimeError("No usable road geometries found.")


roads = gpd.GeoDataFrame(
    features,
    geometry="geometry",
    crs="EPSG:4326"
)


roads.to_file(
    OUTPUT_FILE,
    driver="GeoJSON"
)


print()
print("===================================")
print("OSM ROAD NETWORK")
print("===================================")

print("Total road segments:", len(roads))
print("CRS:", roads.crs)

print()
print("Road types:")
print(
    roads["highway"]
    .value_counts()
    .head(15)
)

print()
print("Saved:")
print(OUTPUT_FILE)