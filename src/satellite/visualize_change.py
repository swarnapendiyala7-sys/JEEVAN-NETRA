import rasterio
import matplotlib.pyplot as plt

INPUT_FILE = "vijayawada_change.tiff"
OUTPUT_FILE = "vijayawada_change_preview.png"

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1)
    bounds = src.bounds
    crs = src.crs

print("CRS:", crs)
print("Bounds:", bounds)
print("Shape:", data.shape)

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

plt.colorbar(label="Significant Change")
plt.title("JEEVAN-NETRA – Sentinel-1 Radar Change Map")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=150)
plt.show()

print()
print("Preview saved:", OUTPUT_FILE)