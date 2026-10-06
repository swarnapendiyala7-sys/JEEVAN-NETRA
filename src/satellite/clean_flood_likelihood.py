import rasterio
import numpy as np
from scipy import ndimage

# ---------------------------------------------------------
# JEEVAN-NETRA 2.0
# Gentle Spatial Cleaning of Flood Candidate Pixels
# ---------------------------------------------------------

INPUT_FILE = "vijayawada_flood_likelihood.tiff"
OUTPUT_FILE = "vijayawada_flood_clean.tiff"

print("Reading flood-likelihood candidate map...")

with rasterio.open(INPUT_FILE) as src:
    data = src.read(1)
    profile = src.profile.copy()
    crs = src.crs

print("Input shape:", data.shape)
print("CRS:", crs)


# ---------------------------------------------------------
# 1. Original candidate mask
# ---------------------------------------------------------

candidate = data > 0

before_pixels = int(np.sum(candidate))

print()
print("Before cleaning:")
print("Candidate pixels:", before_pixels)


# ---------------------------------------------------------
# 2. Gentle neighborhood filter
#
# 3x3 neighborhood
# Keep a pixel if at least 2 pixels in its neighborhood
# are also candidates.
# ---------------------------------------------------------

kernel = np.ones((3, 3), dtype=np.uint8)

neighbor_count = ndimage.convolve(
    candidate.astype(np.uint8),
    kernel,
    mode="constant",
    cval=0
)

cleaned = (
    candidate
    & (neighbor_count >= 2)
)


# ---------------------------------------------------------
# 3. Connected components
# ---------------------------------------------------------

labeled, number_of_regions = ndimage.label(cleaned)

region_sizes = np.bincount(labeled.ravel())


# ---------------------------------------------------------
# 4. Remove only very tiny regions
#
# We use a small minimum size for this first pass.
# ---------------------------------------------------------

MIN_REGION_SIZE = 5

cleaned_final = np.zeros_like(cleaned, dtype=bool)

for region_id in range(1, number_of_regions + 1):

    size = region_sizes[region_id]

    if size >= MIN_REGION_SIZE:
        cleaned_final[labeled == region_id] = True


# ---------------------------------------------------------
# 5. Convert to GeoTIFF-compatible format
# ---------------------------------------------------------

output = cleaned_final.astype(np.uint8)

after_pixels = int(np.sum(output))

total_pixels = output.size


# ---------------------------------------------------------
# 6. Statistics
# ---------------------------------------------------------

before_percentage = (
    before_pixels / total_pixels
) * 100

after_percentage = (
    after_pixels / total_pixels
) * 100


print()
print("After gentle cleaning:")
print("Candidate pixels:", after_pixels)

print(
    "Candidate area:",
    round(after_percentage, 2),
    "%"
)

print(
    "Removed candidate pixels:",
    before_pixels - after_pixels
)

print(
    "Connected regions:",
    number_of_regions
)


# ---------------------------------------------------------
# 7. Save georeferenced output
# ---------------------------------------------------------

profile.update(
    dtype=rasterio.uint8,
    count=1,
    compress="lzw"
)

with rasterio.open(
    OUTPUT_FILE,
    "w",
    **profile
) as dst:

    dst.write(output, 1)


print()
print("Cleaned map saved:")
print(OUTPUT_FILE)

print()
print("NOTE:")
print(
    "This is a spatially cleaned satellite-derived "
    "water/flood candidate layer."
)

print(
    "It is not a confirmed flood classification."
)