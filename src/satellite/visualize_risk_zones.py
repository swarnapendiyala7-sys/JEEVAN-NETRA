import rasterio
import matplotlib.pyplot as plt

INPUT_FILE = "vijayawada_risk_zones.tiff"
OUTPUT_FILE = "vijayawada_risk_zones_preview.png"

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1)
    bounds = src.bounds
    crs = src.crs

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

plt.colorbar(
    label="High-Risk Evidence Zone"
)

plt.title(
    "JEEVAN-NETRA – High Radar/Risk Evidence Zones"
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
print("CRS:", crs)
print("Shape:", data.shape)
print("Risk-zone pixels:", int(data.sum()))
print()
print("Preview saved:", OUTPUT_FILE)