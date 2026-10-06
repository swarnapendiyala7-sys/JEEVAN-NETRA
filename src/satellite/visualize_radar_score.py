import rasterio
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILE = "vijayawada_radar_change_score.tiff"
OUTPUT_FILE = "vijayawada_radar_change_score_preview.png"

print("Reading radar change score...")

with rasterio.open(INPUT_FILE) as src:

    data = src.read(1)

    bounds = src.bounds
    crs = src.crs

print("CRS:", crs)
print("Bounds:", bounds)
print("Shape:", data.shape)


# ---------------------------------------------------------
# Use percentile limits so extreme pixels do not dominate
# the visualization.
# ---------------------------------------------------------

lower = np.percentile(data, 2)
upper = np.percentile(data, 98)

print("Display minimum:", lower)
print("Display maximum:", upper)


# ---------------------------------------------------------
# Create continuous heatmap
# ---------------------------------------------------------

plt.figure(figsize=(10, 8))

image = plt.imshow(
    data,
    extent=[
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ],
    origin="upper",
    vmin=lower,
    vmax=upper
)

plt.colorbar(
    image,
    label="Radar Change Score"
)

plt.title(
    "JEEVAN-NETRA – Sentinel-1 Radar Change Score"
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=150
)

plt.show()

print()
print("Preview saved:")
print(OUTPUT_FILE)