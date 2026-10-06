import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ROADS_FILE = BASE_DIR / "vijayawada_road_risk_scored.geojson"

OUTPUT_IMAGE = BASE_DIR / "vijayawada_scored_road_risk.png"


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading scored road network...")

roads = gpd.read_file(ROADS_FILE)

print(f"Roads loaded: {len(roads)}")


# ============================================================
# CREATE MAP
# ============================================================

print("\nCreating scored road-risk map...")

fig, ax = plt.subplots(
    figsize=(14, 10)
)


# Plot roads using normalized risk
roads.plot(
    ax=ax,
    column="normalized_risk",
    linewidth=1.0,
    legend=True,
    legend_kwds={
        "label": "Satellite-derived road risk evidence",
        "orientation": "vertical"
    }
)


# ============================================================
# TITLE
# ============================================================

ax.set_title(
    "JEEVAN-NETRA 2.0\n"
    "Road-Level Satellite Risk Evidence",
    fontsize=16,
    fontweight="bold"
)


ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.grid(
    True,
    alpha=0.2
)


# ============================================================
# SAVE
# ============================================================

plt.tight_layout()

plt.savefig(
    OUTPUT_IMAGE,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


print("\n===================================")
print("SCORED ROAD MAP CREATED")
print("===================================")

print("Saved:")
print(OUTPUT_IMAGE)

print("\nRisk levels included:")

print(
    roads["risk_level"]
    .value_counts()
)

print(
    "\nNOTE:"
    "\nThe map represents satellite-derived "
    "risk evidence associated with roads."
    "\nIt does not confirm that a road is flooded."
)