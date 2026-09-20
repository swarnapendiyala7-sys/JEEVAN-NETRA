import streamlit as st
import pandas as pd
from pathlib import Path

from src.ui_theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JEEVAN-NETRA | Incidents",
    page_icon="🚨",
    layout="wide"
)

apply_theme()


# ============================================================
# INCIDENT COMMAND CENTER THEME
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       INCIDENT COMMAND CENTER
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(0, 180, 255, 0.08),
                transparent 27%
            ),
            radial-gradient(
                circle at 95% 12%,
                rgba(120, 70, 255, 0.08),
                transparent 30%
            ),
            #0b1220;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(23, 47, 74, 0.95),
                rgba(11, 27, 46, 0.98)
            );

        border:
            1px solid rgba(70, 190, 250, 0.20);

        border-radius: 18px;
        padding: 20px;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.16);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        border-color:
            rgba(70, 210, 255, 0.55);

        box-shadow:
            0 14px 35px rgba(0, 170, 255, 0.12);
    }


    /* =====================================================
       FILTER CONTROLS
       ===================================================== */

    div[data-baseweb="select"] > div {
        background:
            rgba(13, 29, 48, 0.96) !important;

        border:
            1px solid rgba(70, 185, 245, 0.22) !important;

        border-radius: 12px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color:
            rgba(70, 210, 255, 0.55) !important;

        box-shadow:
            0 0 18px rgba(0, 180, 255, 0.08);
    }


    /* =====================================================
       DATA TABLE
       ===================================================== */

    div[data-testid="stDataFrame"] {
        border:
            1px solid rgba(70, 190, 250, 0.16);

        border-radius: 16px;

        overflow: hidden;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.14);
    }


    /* =====================================================
       CHART CONTAINERS
       ===================================================== */

    div[data-testid="stVegaLiteChart"] {
        background:
            rgba(13, 28, 46, 0.60);

        border:
            1px solid rgba(70, 190, 250, 0.13);

        border-radius: 17px;

        padding: 8px;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.12);
    }


    /* =====================================================
       INFORMATION / DESCRIPTION BOXES
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 15px !important;
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    div[data-testid="stExpander"] {
        background:
            rgba(14, 30, 49, 0.72) !important;

        border:
            1px solid rgba(70, 190, 250, 0.16) !important;

        border-radius: 16px !important;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(70, 190, 250, 0.28),
                transparent
            );
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

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

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

INCIDENT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "flood_inventory_clean.csv"
)

IMPACT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "flood_impact_features.csv"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_value(value, unavailable_text="Not reported"):
    """Convert missing/invalid values into user-friendly display text."""

    if pd.isna(value):
        return unavailable_text

    if isinstance(value, str):
        value = value.strip()

        if value.lower() in {
            "nan",
            "none",
            "null",
            ""
        }:
            return unavailable_text

    return value


def clean_score(value):
    """Clean historical impact scores for display."""

    if pd.isna(value):
        return "Not available"

    try:
        numeric_value = float(value)

        if numeric_value == -1:
            return "Not available"

        if numeric_value.is_integer():
            return str(int(numeric_value))

        return f"{numeric_value:.2f}"

    except (ValueError, TypeError):
        return "Not available"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    incidents = pd.read_csv(
        INCIDENT_PATH
    )

    impact = pd.read_csv(
        IMPACT_PATH
    )

    if (
        "UEI" in incidents.columns
        and
        "UEI" in impact.columns
    ):

        impact_columns = [
            "UEI",
            "Historical_Impact_Level",
            "Historical_Impact_Score"
        ]

        impact_columns = [
            col
            for col in impact_columns
            if col in impact.columns
        ]

        impact_small = impact[
            impact_columns
        ].copy()

        incidents = incidents.merge(
            impact_small,
            on="UEI",
            how="left"
        )

    if "Historical_Impact_Level" not in incidents.columns:
        incidents["Historical_Impact_Level"] = "Unknown"

    incidents["Historical_Impact_Level"] = (
        incidents["Historical_Impact_Level"]
        .fillna("Unknown")
        .astype(str)
    )

    if "Start Date" in incidents.columns:

        incidents["Start Date"] = pd.to_datetime(
            incidents["Start Date"],
            errors="coerce"
        )

    if "End Date" in incidents.columns:

        incidents["End Date"] = pd.to_datetime(
            incidents["End Date"],
            errors="coerce"
        )

    return incidents


df = load_data()


# ============================================================
# CALCULATE SUMMARY
# ============================================================

total_incidents = len(df)

high_impact = (
    df["Historical_Impact_Level"]
    .isin(["High", "Extreme"])
    .sum()
)

extreme_impact = (
    df["Historical_Impact_Level"] == "Extreme"
).sum()

events_with_end_date = (
    df["End Date"].notna().sum()
    if "End Date" in df.columns
    else 0
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🚨 Incident Command Center")

st.caption(
    "Historical flood-event intelligence from the "
    "India Flood Inventory (IFI) v3."
)

st.info(
    "📡 Historical Incident Intelligence Active • "
    "Monitoring recorded flood events and their reported impacts."
)

st.divider()


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌊 Total Incidents",
        f"{total_incidents:,}",
        "Historical records"
    )

with col2:
    st.metric(
        "🟠 High Impact",
        f"{high_impact:,}",
        "High + Extreme"
    )

with col3:
    st.metric(
        "🔴 Extreme Impact",
        f"{extreme_impact:,}",
        "Highest reported impact"
    )

with col4:
    st.metric(
        "📅 Events With End Date",
        f"{events_with_end_date:,}",
        "Recorded duration"
    )


st.divider()


# ============================================================
# FILTERS
# ============================================================

st.subheader("🔎 Incident Intelligence Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)


with filter_col1:

    states = sorted(
        df["State"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_state = st.selectbox(
        "State",
        ["All States"] + states
    )


with filter_col2:

    causes = sorted(
        df["Main_Cause_Clean"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_cause = st.selectbox(
        "Main Cause",
        ["All Causes"] + causes
    )


with filter_col3:

    impact_levels = [
        "All Impact Levels",
        "Unknown",
        "No Fatality Reported",
        "Low",
        "Moderate",
        "High",
        "Extreme"
    ]

    selected_impact = st.selectbox(
        "Historical Impact",
        impact_levels
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_state != "All States":

    filtered_df = filtered_df[
        filtered_df["State"].astype(str)
        == selected_state
    ]


if selected_cause != "All Causes":

    filtered_df = filtered_df[
        filtered_df["Main_Cause_Clean"].astype(str)
        == selected_cause
    ]


if selected_impact != "All Impact Levels":

    filtered_df = filtered_df[
        filtered_df["Historical_Impact_Level"]
        == selected_impact
    ]


# ============================================================
# INCIDENT TABLE
# ============================================================

st.subheader(
    f"📋 Incident Records ({len(filtered_df):,})"
)


display_columns = [
    "UEI",
    "Start Date",
    "End Date",
    "State",
    "Districts",
    "Main_Cause_Clean",
    "Historical_Impact_Level",
    "Human fatality",
    "Human injured",
    "Human Displaced"
]

display_columns = [
    col
    for col in display_columns
    if col in filtered_df.columns
]

display_df = filtered_df[
    display_columns
].copy()


if "Start Date" in display_df.columns:

    display_df["Start Date"] = (
        display_df["Start Date"]
        .dt.strftime("%Y-%m-%d")
        .fillna("Not reported")
    )


if "End Date" in display_df.columns:

    display_df["End Date"] = (
        display_df["End Date"]
        .dt.strftime("%Y-%m-%d")
        .fillna("Not reported")
    )


for column in display_df.columns:

    if column not in [
        "Start Date",
        "End Date"
    ]:

        display_df[column] = (
            display_df[column]
            .apply(
                lambda value: clean_value(value)
            )
        )


st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)


st.divider()


# ============================================================
# IMPACT DISTRIBUTION
# ============================================================

st.subheader("📊 Historical Impact Distribution")

impact_distribution = (
    df["Historical_Impact_Level"]
    .value_counts()
)

st.bar_chart(
    impact_distribution,
    width="stretch"
)


# ============================================================
# FLOOD EVENT CAUSES
# ============================================================

st.subheader("🌧️ Flood Event Causes")

cause_distribution = (
    df["Main_Cause_Clean"]
    .value_counts()
    .head(10)
)

st.bar_chart(
    cause_distribution,
    width="stretch"
)


st.divider()


# ============================================================
# INCIDENT DETAILS
# ============================================================

st.subheader("🔍 Incident Details")


if len(filtered_df) > 0:

    incident_options = (
        filtered_df["UEI"]
        .astype(str)
        .tolist()
    )

    selected_uei = st.selectbox(
        "Select an incident",
        incident_options
    )

    selected_row = filtered_df[
        filtered_df["UEI"].astype(str)
        == selected_uei
    ].iloc[0]


    detail_col1, detail_col2 = st.columns(2)


    # --------------------------------------------------------
    # EVENT INFORMATION
    # --------------------------------------------------------

    with detail_col1:

        st.markdown("### Event Information")

        st.write(
            f"**UEI:** "
            f"{clean_value(selected_row.get('UEI'))}"
        )

        st.write(
            f"**State:** "
            f"{clean_value(selected_row.get('State'))}"
        )

        st.write(
            f"**District:** "
            f"{clean_value(selected_row.get('Districts'))}"
        )

        st.write(
            f"**Main Cause:** "
            f"{clean_value(selected_row.get('Main_Cause_Clean'))}"
        )


        start_date = selected_row.get(
            "Start Date"
        )

        if pd.isna(start_date):

            start_date_display = "Not reported"

        else:

            start_date_display = pd.to_datetime(
                start_date
            ).strftime("%Y-%m-%d")


        st.write(
            f"**Start Date:** "
            f"{start_date_display}"
        )


        end_date = selected_row.get(
            "End Date"
        )

        if pd.isna(end_date):

            end_date_display = "Not reported"

        else:

            end_date_display = pd.to_datetime(
                end_date
            ).strftime("%Y-%m-%d")


        st.write(
            f"**End Date:** "
            f"{end_date_display}"
        )


        duration = selected_row.get(
            "Duration(Days)"
        )

        duration_display = clean_value(
            duration,
            "Not available"
        )


        if duration_display != "Not available":

            st.write(
                f"**Duration:** "
                f"{duration_display} days"
            )

        else:

            st.write(
                "**Duration:** Not available"
            )


    # --------------------------------------------------------
    # HISTORICAL IMPACT
    # --------------------------------------------------------

    with detail_col2:

        st.markdown("### Historical Impact")

        impact_level = clean_value(
            selected_row.get(
                "Historical_Impact_Level"
            ),
            "Unknown"
        )

        impact_score = clean_score(
            selected_row.get(
                "Historical_Impact_Score"
            )
        )


        st.write(
            f"**Impact Level:** "
            f"{impact_level}"
        )

        st.write(
            f"**Impact Score:** "
            f"{impact_score}"
        )

        st.write(
            f"**Human Fatality:** "
            f"{clean_value(selected_row.get('Human fatality'))}"
        )

        st.write(
            f"**Human Injured:** "
            f"{clean_value(selected_row.get('Human injured'))}"
        )

        st.write(
            f"**Human Displaced:** "
            f"{clean_value(selected_row.get('Human Displaced'))}"
        )

        st.write(
            f"**Animal Fatality:** "
            f"{clean_value(selected_row.get('Animal Fatality'))}"
        )


    # --------------------------------------------------------
    # EVENT DESCRIPTION
    # --------------------------------------------------------

    st.markdown("### 📝 Event Description")

    description = selected_row.get(
        "Description of Casualties/injured"
    )


    if (
        pd.isna(description)
        or str(description).strip() == ""
        or str(description).lower()
        in {"nan", "none", "null"}
    ):

        description = (
            "No description available."
        )


    st.info(str(description))


else:

    st.warning(
        "No incidents match the selected filters."
    )


st.divider()


# ============================================================
# DATASET INFORMATION
# ============================================================

st.subheader("ℹ️ Dataset Information")

st.write(
    "This page uses the India Flood Inventory (IFI) v3 "
    "historical flood-event dataset. Historical impact levels "
    "are derived from reported human-fatality information and "
    "should be interpreted as historical impact signals rather "
    "than exact ground-truth severity labels."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "JEEVAN-NETRA 2.0 • Incident Command Center"
)

st.caption(
    "Historical records are presented for analytical and "
    "decision-support purposes."
)