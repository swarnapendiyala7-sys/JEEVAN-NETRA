import geopandas as gpd
from pathlib import Path
from datetime import datetime


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "vijayawada_road_risk_scored.geojson"

OUTPUT_FILE = BASE_DIR / "vijayawada_authority_alerts.txt"


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading road-risk data...")

roads = gpd.read_file(INPUT_FILE)

print(f"Road records: {len(roads)}")


# ============================================================
# SELECT HIGH-RISK ROADS
# ============================================================

alerts = roads[
    roads["risk_level"].isin(
        ["CRITICAL", "HIGH"]
    )
].copy()

print(
    f"High-priority road records: {len(alerts)}"
)


# ============================================================
# GENERATE ALERT REPORT
# ============================================================

timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write("=" * 60 + "\n")
    file.write("JEEVAN-NETRA 2.0\n")
    file.write("AUTHORITY ROAD-RISK ALERT REPORT\n")
    file.write("=" * 60 + "\n\n")

    file.write(
        f"Generated: {timestamp}\n"
    )

    file.write(
        "Area: Vijayawada, Andhra Pradesh\n"
    )

    file.write(
        "Evidence source: Sentinel-1 satellite + "
        "historical rainfall context + GIS road data\n\n"
    )

    file.write(
        "IMPORTANT:\n"
        "These alerts represent satellite-derived "
        "risk evidence.\n"
        "They are NOT confirmed flood observations.\n"
        "Field verification is recommended before "
        "official road closure or emergency action.\n\n"
    )

    file.write("=" * 60 + "\n\n")


    # --------------------------------------------------------
    # GENERATE INDIVIDUAL ALERTS
    # --------------------------------------------------------

    for index, row in alerts.iterrows():

        road_name = row.get(
            "name",
            "Unnamed Road"
        )

        road_type = row.get(
            "highway",
            "Unknown"
        )

        risk_score = row.get(
            "normalized_risk",
            0
        )

        risk_level = row.get(
            "risk_level",
            "UNKNOWN"
        )


        # Get representative point
        point = row.geometry.representative_point()


        file.write(
            f"ALERT #{index}\n"
        )

        file.write(
            "-" * 40 + "\n"
        )

        file.write(
            f"Road: {road_name}\n"
        )

        file.write(
            f"Road type: {road_type}\n"
        )

        file.write(
            f"Risk score: {risk_score:.2f}/100\n"
        )

        file.write(
            f"Risk level: {risk_level}\n"
        )

        file.write(
            f"Latitude: {point.y:.6f}\n"
        )

        file.write(
            f"Longitude: {point.x:.6f}\n"
        )

        file.write(
            "Evidence: Road intersects a "
            "satellite-derived high-risk zone.\n"
        )

        file.write(
            "Recommended response: "
            "Prioritize field inspection and "
            "traffic-safety assessment.\n\n"
        )


# ============================================================
# SUMMARY
# ============================================================

print("\n===================================")
print("AUTHORITY ALERT REPORT")
print("===================================")

print(
    f"Total roads analyzed: {len(roads)}"
)

print(
    f"Alerts generated: {len(alerts)}"
)

print("\nAlert levels:")

print(
    alerts["risk_level"]
    .value_counts()
)

print("\nSaved:")
print(OUTPUT_FILE)