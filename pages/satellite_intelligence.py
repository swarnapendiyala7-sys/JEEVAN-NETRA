import streamlit as st
import geopandas as gpd
import pandas as pd
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Satellite Intelligence",
    page_icon="🛰️",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

ROAD_FILE = BASE_DIR / "vijayawada_road_risk_scored.geojson"
ALERT_FILE = BASE_DIR / "vijayawada_authority_alerts.txt"
MAP_FILE = BASE_DIR / "vijayawada_road_risk_map.png"
SCORED_MAP_FILE = BASE_DIR / "vijayawada_scored_road_risk.png"
SATELLITE_IMAGE = BASE_DIR / "vijayawada_sentinel1.png"


# ============================================================
# TITLE
# ============================================================

st.title("🛰️ Satellite Intelligence")

st.markdown(
    """
    **JEEVAN-NETRA 2.0**

    Satellite-based environmental risk evidence is combined
    with rainfall context and real-world road GIS data to
    identify potentially affected road segments.
    """
)


st.warning(
    "⚠️ These results represent satellite-derived risk evidence "
    "and are not confirmed flood observations. Field verification "
    "is recommended before official emergency action."
)


# ============================================================
# LOAD ROAD DATA
# ============================================================

@st.cache_data
def load_roads():

    if not ROAD_FILE.exists():
        return None

    return gpd.read_file(ROAD_FILE)


roads = load_roads()


if roads is None:

    st.error(
        "Road risk data not found. "
        "Run road_risk_score.py first."
    )

    st.stop()


# ============================================================
# METRICS
# ============================================================

total_roads = len(roads)

critical = len(
    roads[roads["risk_level"] == "CRITICAL"]
)

high = len(
    roads[roads["risk_level"] == "HIGH"]
)

medium = len(
    roads[roads["risk_level"] == "MEDIUM"]
)

low = len(
    roads[roads["risk_level"] == "LOW"]
)


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Roads Analyzed",
    total_roads
)

col2.metric(
    "Critical",
    critical
)

col3.metric(
    "High",
    high
)

col4.metric(
    "Medium",
    medium
)

col5.metric(
    "Low",
    low
)


# ============================================================
# SATELLITE IMAGE
# ============================================================

st.divider()

st.subheader("🛰️ Sentinel-1 Satellite Evidence")

if SATELLITE_IMAGE.exists():

    st.image(
        str(SATELLITE_IMAGE),
        caption="Sentinel-1 radar imagery for the study area",
        use_container_width=True
    )

else:

    st.info(
        "Sentinel-1 image not found."
    )


# ============================================================
# ROAD RISK MAP
# ============================================================

st.divider()

st.subheader(
    "🗺️ Potentially Affected Road Network"
)

if MAP_FILE.exists():

    st.image(
        str(MAP_FILE),
        caption=(
            "OSM road network intersecting "
            "satellite-derived risk zones"
        ),
        use_container_width=True
    )

else:

    st.info(
        "Road risk map not found."
    )


# ============================================================
# SCORED ROAD MAP
# ============================================================

st.divider()

st.subheader(
    "📊 Road-Level Risk Evidence"
)

if SCORED_MAP_FILE.exists():

    st.image(
        str(SCORED_MAP_FILE),
        caption=(
            "Road-level satellite-derived "
            "risk evidence"
        ),
        use_container_width=True
    )

else:

    st.info(
        "Scored road map not found."
    )


# ============================================================
# HIGH PRIORITY ROADS
# ============================================================

st.divider()

st.subheader(
    "🚨 High-Priority Road Alerts"
)

priority_roads = roads[
    roads["risk_level"].isin(
        ["CRITICAL", "HIGH"]
    )
].copy()


display_columns = [
    "name",
    "highway",
    "normalized_risk",
    "risk_level"
]


available_columns = [
    column
    for column in display_columns
    if column in priority_roads.columns
]


if len(priority_roads) > 0:

    table = priority_roads[
        available_columns
    ].copy()

    if "normalized_risk" in table.columns:

        table["normalized_risk"] = (
            table["normalized_risk"]
            .round(2)
        )

    table = table.rename(
        columns={
            "name": "Road",
            "highway": "Road Type",
            "normalized_risk": "Risk Score",
            "risk_level": "Risk Level"
        }
    )

    st.dataframe(
        table.head(100),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No high-priority roads detected."
    )


# ============================================================
# AUTHORITY ALERT REPORT
# ============================================================

st.divider()

st.subheader(
    "📄 Authority Alert Report"
)

if ALERT_FILE.exists():

    with open(
        ALERT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        alert_text = file.read()


    st.download_button(
        label="⬇️ Download Authority Alert Report",
        data=alert_text,
        file_name="JEEVAN_NETRA_Authority_Alerts.txt",
        mime="text/plain"
    )


    with st.expander(
        "View Alert Report"
    ):

        st.text(
            alert_text[:15000]
        )

else:

    st.info(
        "Authority alert report not found."
    )


# ============================================================
# METHODOLOGY
# ============================================================

st.divider()

st.subheader(
    "🔬 Intelligence Pipeline"
)

st.markdown(
    """
    **1. Sentinel-1 Radar**

    Real Sentinel-1 GRD data is retrieved through
    Copernicus Data Space.

    **2. Radar Change Analysis**

    Before/after radar observations are compared
    to identify surface-change evidence.

    **3. Multi-Modal Risk**

    Radar evidence is combined with historical
    rainfall context.

    **4. Risk Zones**

    High-evidence areas are extracted spatially.

    **5. Road GIS**

    OpenStreetMap road data is intersected with
    the risk zones.

    **6. Road Risk Scoring**

    Potentially affected road segments receive
    a normalized risk-evidence score.

    **7. Authority Alerts**

    High and critical road records are converted
    into a structured alert report for field
    verification and response planning.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    f"JEEVAN-NETRA 2.0 • Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)