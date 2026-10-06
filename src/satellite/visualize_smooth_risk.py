import rasterio
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILE = "vijayawada_multimodal_risk_smooth.tiff"
OUTPUT_FILE = "vijayawada_multimodal_risk_smooth_preview.png"

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1)
    bounds = src.bounds
    crs = src.crs

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
    label="Smoothed Multi-Modal Risk Evidence"
)

plt.title(
    "JEEVAN-NETRA – Smoothed Satellite + Rainfall Risk"
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
print("Preview saved:", OUTPUT_FILE)