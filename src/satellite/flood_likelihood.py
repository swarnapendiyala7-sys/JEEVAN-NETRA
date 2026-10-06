import rasterio
import numpy as np

# ---------------------------------------------------------
# JEEVAN-NETRA 2.0
# Sentinel-1 Water / Flood Likelihood Analysis
# ---------------------------------------------------------

BEFORE_FILE = "vijayawada_before.tiff"
AFTER_FILE = "vijayawada_after.tiff"

OUTPUT_FILE = "vijayawada_flood_likelihood.tiff"


print("Reading Sentinel-1 radar data...")

with rasterio.open(BEFORE_FILE) as before_src:
    before_vv = before_src.read(1).astype("float32")
    profile = before_src.profile.copy()

with rasterio.open(AFTER_FILE) as after_src:
    after_vv = after_src.read(1).astype("float32")


print("Before shape:", before_vv.shape)
print("After shape:", after_vv.shape)


# ---------------------------------------------------------
# 1. Remove invalid values
# ---------------------------------------------------------

before_vv = np.nan_to_num(
    before_vv,
    nan=0.0,
    posinf=0.0,
    neginf=0.0
)

after_vv = np.nan_to_num(
    after_vv,
    nan=0.0,
    posinf=0.0,
    neginf=0.0
)


# ---------------------------------------------------------
# 2. Calculate radar ratio
#
# Water surfaces generally produce lower radar
# backscatter than many surrounding land surfaces.
#
# We therefore look for pixels where the AFTER value
# decreases strongly compared with BEFORE.
# ---------------------------------------------------------

epsilon = 1e-6

ratio = after_vv / (before_vv + epsilon)


# ---------------------------------------------------------
# 3. Detect strong decrease
#
# ratio < 0.5 means the after value is less than
# approximately half of the before value.
#
# This is a candidate threshold, NOT a scientifically
# validated flood threshold.
# ---------------------------------------------------------

water_candidate = ratio < 0.5


# ---------------------------------------------------------
# 4. Remove extremely weak/noisy pixels
# ---------------------------------------------------------

valid_pixels = (
    (before_vv > epsilon)
    & (after_vv > epsilon)
)

flood_likelihood = (
    water_candidate
    & valid_pixels
)


# ---------------------------------------------------------
# 5. Convert Boolean result to 0/1
# ---------------------------------------------------------

output = flood_likelihood.astype("uint8")


# ---------------------------------------------------------
# 6. Calculate statistics
# ---------------------------------------------------------

total_pixels = output.size
candidate_pixels = np.sum(output)

candidate_percentage = (
    candidate_pixels / total_pixels
) * 100


print()
print("Flood-likelihood candidate analysis")
print("-----------------------------------")
print("Candidate pixels:", candidate_pixels)
print("Total pixels:", total_pixels)
print(
    "Candidate area:",
    round(candidate_percentage, 2),
    "%"
)


# ---------------------------------------------------------
# 7. Save georeferenced GeoTIFF
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
print("Flood-likelihood map saved:")
print(OUTPUT_FILE)

print()
print("IMPORTANT:")
print(
    "This is a satellite-derived water/flood candidate map."
)
print(
    "It is NOT yet a confirmed flood classification."
)