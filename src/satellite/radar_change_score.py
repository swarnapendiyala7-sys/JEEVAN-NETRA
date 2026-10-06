import rasterio
import numpy as np

# ---------------------------------------------------------
# JEEVAN-NETRA 2.0
# Sentinel-1 VV + VH Radar Change Score
# ---------------------------------------------------------

BEFORE_FILE = "vijayawada_before.tiff"
AFTER_FILE = "vijayawada_after.tiff"

OUTPUT_FILE = "vijayawada_radar_change_score.tiff"


print("Reading Sentinel-1 VV + VH data...")


# ---------------------------------------------------------
# 1. Read BEFORE image
# ---------------------------------------------------------

with rasterio.open(BEFORE_FILE) as src:

    before_vv = src.read(1).astype("float32")
    before_vh = src.read(2).astype("float32")

    profile = src.profile.copy()
    bounds = src.bounds
    crs = src.crs


# ---------------------------------------------------------
# 2. Read AFTER image
# ---------------------------------------------------------

with rasterio.open(AFTER_FILE) as src:

    after_vv = src.read(1).astype("float32")
    after_vh = src.read(2).astype("float32")


print("VV shape:", before_vv.shape)
print("VH shape:", before_vh.shape)


# ---------------------------------------------------------
# 3. Remove invalid values
# ---------------------------------------------------------

before_vv = np.nan_to_num(
    before_vv,
    nan=0.0,
    posinf=0.0,
    neginf=0.0
)

before_vh = np.nan_to_num(
    before_vh,
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

after_vh = np.nan_to_num(
    after_vh,
    nan=0.0,
    posinf=0.0,
    neginf=0.0
)


# ---------------------------------------------------------
# 4. Calculate relative decrease
#
# A decrease in radar backscatter can occur when
# previously rough/dry surfaces become smoother or wetter.
#
# This is a candidate signal, NOT proof of flooding.
# ---------------------------------------------------------

epsilon = 1e-6

vv_decrease = (
    (before_vv - after_vv)
    / (before_vv + epsilon)
)

vh_decrease = (
    (before_vh - after_vh)
    / (before_vh + epsilon)
)


# ---------------------------------------------------------
# 5. Limit extreme numerical values
# ---------------------------------------------------------

vv_decrease = np.clip(
    vv_decrease,
    0,
    1
)

vh_decrease = np.clip(
    vh_decrease,
    0,
    1
)


# ---------------------------------------------------------
# 6. Combine VV and VH
#
# VV gets slightly higher weight because it often provides
# strong surface-scattering information.
# ---------------------------------------------------------

radar_score = (
    0.6 * vv_decrease
    +
    0.4 * vh_decrease
)


# ---------------------------------------------------------
# 7. Convert to 0–100 score
# ---------------------------------------------------------

radar_score = radar_score * 100


# ---------------------------------------------------------
# 8. Statistics
# ---------------------------------------------------------

valid = np.isfinite(radar_score)

values = radar_score[valid]

print()
print("Radar Change Score")
print("------------------")
print("Minimum:", float(np.min(values)))
print("Maximum:", float(np.max(values)))
print("Mean:", float(np.mean(values)))
print("Median:", float(np.median(values)))


# ---------------------------------------------------------
# 9. Data-driven high-change threshold
#
# 90th percentile = strongest 10% of observed change.
# This is an anomaly threshold, not a flood threshold.
# ---------------------------------------------------------

threshold = np.percentile(
    values,
    90
)

print()
print(
    "90th percentile threshold:",
    float(threshold)
)


# ---------------------------------------------------------
# 10. Save continuous radar score
# ---------------------------------------------------------

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

    dst.write(
        radar_score.astype("float32"),
        1
    )


print()
print("Radar change score saved:")
print(OUTPUT_FILE)

print()
print("IMPORTANT:")
print(
    "This is a continuous radar-change/anomaly score."
)

print(
    "It is NOT a confirmed flood probability."
)