import numpy as np
import rasterio


BEFORE_FILE = "vijayawada_before.tiff"
AFTER_FILE = "vijayawada_after.tiff"

OUTPUT_FILE = "vijayawada_change.tiff"


def main():

    print("Reading Sentinel-1 data...")

    with rasterio.open(BEFORE_FILE) as before_src:
        before = before_src.read()
        profile = before_src.profile.copy()

    with rasterio.open(AFTER_FILE) as after_src:
        after = after_src.read()

    print("Before shape:", before.shape)
    print("After shape:", after.shape)

    # Sentinel-1 output:
    # Band 1 = VV
    # Band 2 = VH

    before_vv = before[0]
    before_vh = before[1]

    after_vv = after[0]
    after_vh = after[1]

    # Avoid invalid numerical values
    valid = (
        np.isfinite(before_vv)
        & np.isfinite(before_vh)
        & np.isfinite(after_vv)
        & np.isfinite(after_vh)
    )

    # Absolute change
    vv_change = np.abs(after_vv - before_vv)
    vh_change = np.abs(after_vh - before_vh)

    # Combine VV and VH change
    combined_change = (vv_change + vh_change) / 2

    # Remove invalid pixels
    combined_change[~valid] = np.nan

    # Basic statistics
    valid_values = combined_change[np.isfinite(combined_change)]

    print("\nChange statistics:")
    print("Minimum:", np.nanmin(valid_values))
    print("Maximum:", np.nanmax(valid_values))
    print("Mean:", np.nanmean(valid_values))
    print("Median:", np.nanmedian(valid_values))

    # Use the 90th percentile as a data-driven
    # threshold for significant change.
    threshold = np.nanpercentile(valid_values, 90)

    print("\nChange threshold:", threshold)

    change_mask = (
        combined_change >= threshold
    ).astype(np.uint8)

    change_mask[~valid] = 0

    changed_pixels = np.sum(change_mask == 1)
    valid_pixels = np.sum(valid)

    if valid_pixels > 0:
        changed_percentage = (
            changed_pixels / valid_pixels
        ) * 100
    else:
        changed_percentage = 0

    print(
        f"Significant-change area: "
        f"{changed_percentage:.2f}%"
    )

    # Save geospatial change map
    profile.update(
        count=1,
        dtype=rasterio.uint8,
        nodata=0
    )

    with rasterio.open(
        OUTPUT_FILE,
        "w",
        **profile
    ) as dst:
        dst.write(change_mask, 1)

    print("\nChange map saved:")
    print(OUTPUT_FILE)

    print("\nIMPORTANT:")
    print(
        "This is a radar-change map, "
        "not yet a confirmed flood map."
    )


if __name__ == "__main__":
    main()