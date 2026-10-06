import numpy as np
import rasterio
from scipy.ndimage import gaussian_filter

INPUT_FILE = "vijayawada_multimodal_risk.tiff"
OUTPUT_FILE = "vijayawada_multimodal_risk_smooth.tiff"

print("Reading multi-modal risk layer...")

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1).astype(np.float32)
    profile = src.profile.copy()

print("Input shape:", data.shape)

# ------------------------------------------------------------
# Spatial smoothing
# ------------------------------------------------------------

# sigma=3 reduces isolated pixel-level noise while
# preserving larger spatial patterns.
smooth = gaussian_filter(data, sigma=3)

smooth = np.clip(
    smooth,
    0,
    100
).astype(np.float32)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

profile.update(
    dtype="float32",
    count=1,
    compress="lzw"
)

with rasterio.open(
    OUTPUT_FILE,
    "w",
    **profile
) as dst:
    dst.write(smooth, 1)

print()
print("Smoothed risk layer created.")
print("Minimum:", round(float(np.nanmin(smooth)), 2))
print("Maximum:", round(float(np.nanmax(smooth)), 2))
print("Mean:", round(float(np.nanmean(smooth)), 2))
print()
print("Saved:", OUTPUT_FILE)