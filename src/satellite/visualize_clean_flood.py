import rasterio
import matplotlib.pyplot as plt

INPUT_FILE = "vijayawada_flood_clean.tiff"
OUTPUT_FILE = "vijayawada_flood_clean_preview.png"

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1)
    bounds = src.bounds
    crs = src.crs

print("CRS:", crs)
print("Bounds:", bounds)
print("Shape:", data.shape)
print("Candidate pixels:", int(data.sum()))

plt.figure(figsize=(10, 8))

plt.imshow(
    data,
    extent=[
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ],
    origin="upper"
)

plt.colorbar(label="Flood / Water Candidate")
plt.title(
    "JEEVAN-NETRA – Cleaned Sentinel-1 "
    "Flood-Likelihood Candidate Map"
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
print("Preview saved:", OUTPUT_FILE)