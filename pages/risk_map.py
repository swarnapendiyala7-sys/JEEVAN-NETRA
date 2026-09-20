import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path

from src.ui_theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Risk Map | JEEVAN-NETRA",
    page_icon="🗺️",
    layout="wide"
)

apply_theme()


# ============================================================
# SMART CITY INTELLIGENCE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Risk Map page */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(0, 190, 255, 0.09),
                transparent 27%
            ),
            radial-gradient(
                circle at 95% 8%,
                rgba(110, 80, 255, 0.08),
                transparent 28%
            ),
            #0b1220;
    }

    /* Smooth native metric cards */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(23, 48, 76, 0.94),
                rgba(12, 28, 48, 0.97)
            );

        border: 1px solid rgba(76, 194, 255, 0.20);
        border-radius: 18px;
        padding: 20px;

        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);

        border-color:
            rgba(76, 210, 255, 0.55);

        box-shadow:
            0 14px 35px rgba(0, 170, 255, 0.12);
    }

    div[data-testid="stMetricLabel"] {
        color: #8fa9c1 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f4fbff !important;
        font-weight: 850 !important;
    }


    /* Select box */

    div[data-baseweb="select"] > div {
        background:
            rgba(13, 29, 48, 0.96) !important;

        border:
            1px solid rgba(76, 190, 245, 0.22) !important;

        border-radius: 12px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color:
            rgba(76, 210, 255, 0.55) !important;

        box-shadow:
            0 0 18px rgba(0, 180, 255, 0.08);
    }


    /* Map area */

    div[data-testid="stDeckGlJsonChart"] {
        border:
            1px solid rgba(76, 195, 255, 0.20);

        border-radius: 18px;

        overflow: hidden;

        box-shadow:
            0 14px 40px rgba(0, 0, 0, 0.18);
    }


    /* Data table */

    div[data-testid="stDataFrame"] {
        border:
            1px solid rgba(76, 195, 255, 0.16);

        border-radius: 16px;

        overflow: hidden;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.14);
    }


    /* Expander */

    div[data-testid="stExpander"] {
        background:
            rgba(14, 30, 49, 0.75) !important;

        border:
            1px solid rgba(76, 195, 255, 0.16) !important;

        border-radius: 16px !important;
    }


    /* Chart */

    div[data-testid="stVegaLiteChart"] {
        background:
            rgba(13, 28, 46, 0.65);

        border:
            1px solid rgba(74, 190, 245, 0.12);

        border-radius: 17px;

        padding: 8px;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.12);
    }


    /* Buttons */

    .stButton > button {
        border-radius: 11px;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 22px rgba(0, 170, 255, 0.12);
    }


    /* Divider */

    hr {
        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(70, 190, 255, 0.28),
                transparent
            );
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "risk_fusion_features.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


try:
    df = load_data()

except Exception as e:
    st.error("Unable to load Risk Fusion data.")
    st.code(str(e))
    st.stop()


# ============================================================
# STATE COORDINATES
# ============================================================

state_coordinates = {
    "Andhra Pradesh": (15.9129, 79.7400),
    "Arunachal Pradesh": (28.2180, 94.7278),
    "Assam": (26.2006, 92.9376),
    "Bihar": (25.0961, 85.3131),
    "Chhattisgarh": (21.2787, 81.8661),
    "Goa": (15.2993, 74.1240),
    "Gujarat": (22.2587, 71.1924),
    "Haryana": (29.0588, 76.0856),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Jharkhand": (23.6102, 85.2799),
    "Karnataka": (15.3173, 75.7139),
    "Kerala": (10.8505, 76.2711),
    "Madhya Pradesh": (22.9734, 78.6569),
    "Maharashtra": (19.7515, 75.7139),
    "Manipur": (24.6637, 93.9063),
    "Meghalaya": (25.4670, 91.3662),
    "Mizoram": (23.1645, 92.9376),
    "Nagaland": (26.1584, 94.5624),
    "Odisha": (20.9517, 85.0985),
    "Punjab": (31.1471, 75.3412),
    "Rajasthan": (27.0238, 74.2179),
    "Sikkim": (27.5330, 88.5122),
    "Tamil Nadu": (11.1271, 78.6569),
    "Telangana": (18.1124, 79.0193),
    "Tripura": (23.9408, 91.9882),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Uttarakhand": (30.0668, 79.0193),
    "West Bengal": (22.9868, 87.8550),
    "Jammu and Kashmir": (33.7782, 76.5762),
    "Ladakh": (34.1526, 77.5771),
    "Andaman & Nicobar Islands": (11.7401, 92.6586),
    "Chandigarh": (30.7333, 76.7794),
    "Delhi": (28.7041, 77.1025),
    "Puducherry": (11.9416, 79.8083),
    "Dadra and Nagar Haveli and Daman and Diu":
        (20.1809, 73.0169),
    "Lakshadweep": (10.5667, 72.6417)
}


# ============================================================
# ADD COORDINATES
# ============================================================

df["Latitude"] = df["State"].map(
    lambda x: state_coordinates.get(
        x,
        (None, None)
    )[0]
)

df["Longitude"] = df["State"].map(
    lambda x: state_coordinates.get(
        x,
        (None, None)
    )[1]
)

map_df = df.dropna(
    subset=["Latitude", "Longitude"]
).copy()


# ============================================================
# RISK SCORE
# ============================================================

risk_score_map = {
    "LOW": 1,
    "MODERATE": 2,
    "HIGH": 3,
    "CRITICAL": 4
}

map_df["Map_Risk_Score"] = (
    map_df["Overall_Risk_Level"]
    .map(risk_score_map)
)


# ============================================================
# STATE SUMMARY
# ============================================================

state_summary = (
    map_df
    .groupby("State")
    .agg(
        Latitude=("Latitude", "first"),
        Longitude=("Longitude", "first"),
        Risk_Score=("Map_Risk_Score", "max"),
        Risk_Level=("Overall_Risk_Level", "first"),
        Records=("State", "size")
    )
    .reset_index()
)


def get_risk_level(score):

    if score == 4:
        return "CRITICAL"

    if score == 3:
        return "HIGH"

    if score == 2:
        return "MODERATE"

    return "LOW"


state_summary["Risk_Level"] = (
    state_summary["Risk_Score"]
    .apply(get_risk_level)
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🗺️ Smart City Risk Intelligence")

st.caption(
    "Geospatial community risk monitoring powered by "
    "rainfall signals and historical flood intelligence."
)

st.info(
    "🛰️ Risk Intelligence Engine Active • "
    "State-level monitoring mode"
)

st.divider()


# ============================================================
# SUMMARY METRICS
# ============================================================

critical_count = (
    df["Overall_Risk_Level"] == "CRITICAL"
).sum()

high_count = (
    df["Overall_Risk_Level"] == "HIGH"
).sum()

moderate_count = (
    df["Overall_Risk_Level"] == "MODERATE"
).sum()

low_count = (
    df["Overall_Risk_Level"] == "LOW"
).sum()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔴 Critical",
        f"{critical_count:,}",
        "Immediate attention"
    )

with col2:
    st.metric(
        "🟠 High",
        f"{high_count:,}",
        "Priority monitoring"
    )

with col3:
    st.metric(
        "🟡 Moderate",
        f"{moderate_count:,}",
        "Routine monitoring"
    )

with col4:
    st.metric(
        "🟢 Low",
        f"{low_count:,}",
        "Stable conditions"
    )


st.divider()


# ============================================================
# INTERACTIVE MAP
# ============================================================

st.subheader("🛰️ Interactive Community Risk Map")

st.caption(
    "Each marker represents the highest historical risk "
    "identified for that state."
)


# ============================================================
# MARKER COLORS
# ============================================================

def get_marker_color(level):

    if level == "CRITICAL":
        return [255, 60, 60, 220]

    if level == "HIGH":
        return [255, 145, 55, 220]

    if level == "MODERATE":
        return [245, 202, 70, 220]

    return [55, 210, 150, 210]


state_summary["Color"] = (
    state_summary["Risk_Level"]
    .apply(get_marker_color)
)


# ============================================================
# PYDECK
# ============================================================

layer = pdk.Layer(
    "ScatterplotLayer",
    data=state_summary,
    get_position="[Longitude, Latitude]",
    get_radius=45000,
    get_fill_color="Color",
    pickable=True,
    auto_highlight=True,
    radius_min_pixels=7,
    radius_max_pixels=25
)


view_state = pdk.ViewState(
    latitude=22.5,
    longitude=79.0,
    zoom=4.2,
    pitch=0
)


deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": """
        <b>{State}</b><br/>
        Risk Level: {Risk_Level}<br/>
        Records: {Records}
        """,
        "style": {
            "backgroundColor": "#101d31",
            "color": "#eaf8ff"
        }
    }
)


st.pydeck_chart(
    deck,
    width="stretch"
)


# ============================================================
# MAP LEGEND
# ============================================================

st.caption(
    "🔴 CRITICAL    🟠 HIGH    🟡 MODERATE    🟢 LOW"
)


st.divider()


# ============================================================
# STATE FILTER
# ============================================================

st.subheader("🔎 State Intelligence")

selected_state = st.selectbox(
    "Select a State",
    ["All States"]
    +
    sorted(
        df["State"]
        .dropna()
        .unique()
    )
)


if selected_state != "All States":

    selected_df = df[
        df["State"] == selected_state
    ].copy()

else:

    selected_df = df.copy()


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.subheader("📊 Risk Distribution")

risk_distribution = (
    selected_df["Overall_Risk_Level"]
    .value_counts()
    .reindex(
        [
            "CRITICAL",
            "HIGH",
            "MODERATE",
            "LOW"
        ],
        fill_value=0
    )
)

st.bar_chart(
    risk_distribution,
    width="stretch"
)


# ============================================================
# HIGH-RISK RECORDS
# ============================================================

st.subheader("🚨 High-Risk Historical Records")

high_risk_df = selected_df[
    selected_df["Overall_Risk_Level"].isin(
        ["CRITICAL", "HIGH"]
    )
].copy()


if high_risk_df.empty:

    st.success(
        "No Critical or High-risk records found."
    )

else:

    display_columns = [
        "State",
        "Year",
        "Rainfall_Signal",
        "Historical_Flood_Signal",
        "Risk_Fusion_Score",
        "Overall_Risk_Level",
        "Recommended_Action"
    ]

    st.dataframe(
        high_risk_df[
            display_columns
        ]
        .sort_values(
            "Risk_Fusion_Score",
            ascending=False
        )
        .head(20),

        width="stretch",

        hide_index=True
    )


# ============================================================
# INFORMATION
# ============================================================

with st.expander(
    "ℹ️ About this Risk Intelligence Map"
):

    st.write(
        """
        JEEVAN-NETRA currently combines historical rainfall
        risk and historical flood occurrence.

        The system produces four risk levels:

        LOW
        MODERATE
        HIGH
        CRITICAL

        The geographical coordinates used here are
        representative state-level coordinates.

        They are used for visualization and do not represent
        the exact location of an individual flood event.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "JEEVAN-NETRA 2.0 • Smart City Risk Intelligence"
)

st.caption(
    "Risk indicators are decision-support information and "
    "should be interpreted together with official guidance."
)