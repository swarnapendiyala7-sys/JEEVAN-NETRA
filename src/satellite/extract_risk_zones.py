import numpy as np
import rasterio
from scipy import ndimage


INPUT_FILE = "vijayawada_multimodal_risk_smooth.tiff"
OUTPUT_FILE = "vijayawada_risk_zones.tiff"

print("Reading smoothed multi-modal risk...")

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1).astype(np.float32)
    profile = src.profile.copy()

valid = data[np.isfinite(data)]

# ------------------------------------------------------------
# 1. Select only the strongest risk values
# ------------------------------------------------------------

threshold = np.percentile(valid, 90)

print()
print("90th percentile threshold:", round(float(threshold), 2))

candidate = data >= threshold

print("Initial candidate pixels:", int(candidate.sum()))


# ------------------------------------------------------------
# 2. Connected-component analysis
# ------------------------------------------------------------

structure = np.ones((3, 3), dtype=np.uint8)

labels, number_of_regions = ndimage.label(
    candidate,
    structure=structure
)

print("Connected regions:", number_of_regions)


# ------------------------------------------------------------
# 3. Remove very small regions
# ------------------------------------------------------------

MIN_PIXELS = 20

counts = np.bincount(labels.ravel())

clean = np.zeros_like(candidate, dtype=np.uint8)

for region_id in range(1, len(counts)):
    if counts[region_id] >= MIN_PIXELS:
        clean[labels == region_id] = 1


# ------------------------------------------------------------
# 4. Statistics
# ------------------------------------------------------------

print()
print("Minimum region size:", MIN_PIXELS)
print("Risk-zone pixels:", int(clean.sum()))

if clean.sum() > 0:
    print(
        "Risk-zone percentage:",
        round(float(clean.mean() * 100), 2),
        "%"
    )
else:
    print("No sufficiently large risk zones detected.")


# ------------------------------------------------------------
# 5. Save
# ------------------------------------------------------------

profile.update(
    dtype="uint8",
    count=1,
    compress="lzw"
)

with rasterio.open(
    OUTPUT_FILE,
    "w",
    **profile
) as dst:
    dst.write(clean, 1)

print()
print("Risk-zone map saved:")
print(OUTPUT_FILE)

print()
print(
    "NOTE: These are high radar/risk evidence zones,"
)
print(
    "not confirmed flood zones."
)