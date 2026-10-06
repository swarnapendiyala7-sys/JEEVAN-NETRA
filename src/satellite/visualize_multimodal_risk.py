import rasterio
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILE = "vijayawada_multimodal_risk.tiff"
OUTPUT_FILE = "vijayawada_multimodal_risk_preview.png"

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1)
    bounds = src.bounds

valid = data[np.isfinite(data)]

low = np.percentile(valid, 2)
high = np.percentile(valid, 98)

plt.figure(figsize=(10, 8))

plt.imshow(
    data,
    extent=[
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ],
    origin="upper",
    vmin=low,
    vmax=high
)

plt.colorbar(
    label="Multi-Modal Risk Evidence (0-100)"
)

plt.title(
    "JEEVAN-NETRA – Satellite + Rainfall Risk Evidence"
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
print("CRS:", src.crs)
print("Shape:", data.shape)
print("Minimum:", round(float(np.nanmin(data)), 2))
print("Maximum:", round(float(np.nanmax(data)), 2))
print("Mean:", round(float(np.nanmean(data)), 2))
print()
print("Preview saved:", OUTPUT_FILE)