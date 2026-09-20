import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PATH SETUP
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Analytics | JEEVAN-NETRA",
    page_icon="📊",
    layout="wide",
)

# ============================================================
# GLOBAL THEME
# ============================================================
from src.ui_theme import apply_theme

apply_theme()

# ============================================================
# PAGE-SPECIFIC STYLE
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(
                circle at 12% 8%,
                rgba(0, 153, 255, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 88% 10%,
                rgba(125, 70, 255, 0.08),
                transparent 28%
            ),
            #07111f;
    }

    .analytics-title {
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 0.15rem;
    }

    .analytics-subtitle {
        color: #9fb2c8;
        font-size: 1rem;
        margin-bottom: 1.1rem;
    }

    .section-label {
        font-size: 1.15rem;
        font-weight: 750;
        margin-top: 0.35rem;
        margin-bottom: 0.7rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(9, 25, 43, 0.80);
        border: 1px solid rgba(90, 160, 210, 0.16);
        border-radius: 13px;
        padding: 0.9rem 1rem;
    }

    div[data-testid="stMetricLabel"] {
        color: #8fa8bf;
    }

    div[data-testid="stMetricValue"] {
        color: #eaf7ff;
    }

    div[data-testid="stExpander"] {
        background: rgba(8, 23, 40, 0.78);
        border: 1px solid rgba(95, 150, 200, 0.18);
        border-radius: 12px;
    }

    div[data-testid="stAlert"] {
        border-radius: 11px;
    }

    hr {
        border-color: rgba(100, 160, 210, 0.12);
        margin-top: 1.15rem;
        margin-bottom: 1.15rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    '<div class="analytics-title">📊 Risk & Intelligence Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="analytics-subtitle">'
    "Explore historical incidents, rainfall risk, flood signals, "
    "model performance and unified community-risk intelligence."
    "</div>",
    unsafe_allow_html=True,
)

st.info(
    "📊 Analytics Engine Active • Historical datasets + "
    "risk fusion + ML evaluation intelligence"
)

# ============================================================
# DATA FILES
# ============================================================
FLOOD_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "flood_inventory_clean.csv"
)

IMPACT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "flood_impact_features.csv"
)

RISK_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "final_historical_risk.csv"
)

FUSION_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "risk_fusion_features.csv"
)

EVAL_FILE = (
    BASE_DIR
    / "models"
    / "ml"
    / "historical_flood_evaluation.csv"
)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    flood_df = pd.read_csv(FLOOD_FILE)
    impact_df = pd.read_csv(IMPACT_FILE)
    risk_df = pd.read_csv(RISK_FILE)
    fusion_df = pd.read_csv(FUSION_FILE)
    evaluation_df = pd.read_csv(EVAL_FILE)

    return (
        flood_df,
        impact_df,
        risk_df,
        fusion_df,
        evaluation_df,
    )


try:
    (
        flood_df,
        impact_df,
        risk_df,
        fusion_df,
        evaluation_df,
    ) = load_data()

    data_status = True

except Exception as error:
    data_status = False

    st.error(
        f"Unable to load analytics data: {error}"
    )

# ============================================================
# ANALYTICS
# ============================================================
if data_status:

    # ========================================================
    # BASIC COUNTS
    # ========================================================
    total_incidents = len(flood_df)

    # ========================================================
    # HIGH / EXTREME HISTORICAL IMPACT
    # ========================================================
    high_risk_count = 0

    if "Historical_Impact_Level" in impact_df.columns:
        high_risk_count = impact_df[
            impact_df["Historical_Impact_Level"].isin(
                ["High", "Extreme"]
            )
        ].shape[0]

    # ========================================================
    # CRITICAL RISK
    # ========================================================
    critical_count = 0

    if "Final_Risk_Level" in fusion_df.columns:
        critical_count = fusion_df[
            fusion_df["Final_Risk_Level"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "critical"
        ].shape[0]

    # ========================================================
    # ML ACCURACY
    # ========================================================
    model_accuracy = None

    if not evaluation_df.empty:

        metric_column = None

        for column in [
            "Metric",
            "metric",
            "Metrics",
            "metrics",
            "Name",
            "name",
        ]:
            if column in evaluation_df.columns:
                metric_column = column
                break

        value_column = None

        for column in [
            "Value",
            "value",
            "Score",
            "score",
            "Result",
            "result",
            "Accuracy",
            "accuracy",
        ]:
            if column in evaluation_df.columns:
                value_column = column
                break

        if metric_column is not None:

            accuracy_rows = evaluation_df[
                evaluation_df[metric_column]
                .astype(str)
                .str.strip()
                .str.lower()
                == "accuracy"
            ]

            if not accuracy_rows.empty:

                if value_column is not None:

                    try:
                        model_accuracy = float(
                            accuracy_rows.iloc[0][value_column]
                        )
                    except (ValueError, TypeError):
                        model_accuracy = None

                else:

                    numeric_columns = (
                        accuracy_rows
                        .select_dtypes(include="number")
                        .columns
                        .tolist()
                    )

                    if numeric_columns:
                        model_accuracy = float(
                            accuracy_rows.iloc[0][
                                numeric_columns[0]
                            ]
                        )

    # ========================================================
    # TOP METRICS
    # ========================================================
    st.markdown(
        '<div class="section-label">📌 Intelligence Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Historical Incidents",
            f"{total_incidents:,}",
        )

    with col2:
        st.metric(
            "High / Extreme Impact",
            f"{high_risk_count:,}",
        )

    with col3:
        st.metric(
            "Critical Risk Records",
            f"{critical_count:,}",
        )

    with col4:

        if model_accuracy is not None:

            display_accuracy = (
                model_accuracy * 100
                if model_accuracy <= 1
                else model_accuracy
            )

            st.metric(
                "ML Accuracy",
                f"{display_accuracy:.2f}%",
            )

        else:

            st.metric(
                "ML Accuracy",
                "Available",
            )

    # ========================================================
    # HISTORICAL INCIDENT ANALYTICS
    # ========================================================
    st.divider()

    st.markdown(
        '<div class="section-label">'
        "🚨 Historical Incident Analytics"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # TOP CAUSES
    # --------------------------------------------------------
    with col1:

        if "Main Cause" in flood_df.columns:

            cause_counts = (
                flood_df["Main Cause"]
                .fillna("Unknown")
                .value_counts()
                .reset_index()
            )

            cause_counts.columns = [
                "Cause",
                "Count",
            ]

            fig = px.bar(
                cause_counts.head(8),
                x="Count",
                y="Cause",
                orientation="h",
                title="Top Historical Flood Causes",
            )

            fig.update_layout(
                yaxis={
                    "categoryorder": "total ascending"
                },
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=20,
                ),
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

    # --------------------------------------------------------
    # INCIDENTS BY YEAR
    # --------------------------------------------------------
    with col2:

        if "Year" in flood_df.columns:

            year_counts = (
                flood_df["Year"]
                .value_counts()
                .sort_index()
                .reset_index()
            )

            year_counts.columns = [
                "Year",
                "Incidents",
            ]

            fig = px.line(
                year_counts,
                x="Year",
                y="Incidents",
                markers=True,
                title="Historical Incidents by Year",
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=20,
                ),
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

    # ========================================================
    # HISTORICAL IMPACT
    # ========================================================
    st.divider()

    st.markdown(
        '<div class="section-label">'
        "⚠️ Historical Impact Intelligence"
        "</div>",
        unsafe_allow_html=True,
    )

    if "Historical_Impact_Level" in impact_df.columns:

        impact_counts = (
            impact_df["Historical_Impact_Level"]
            .fillna("Unknown")
            .value_counts()
            .reindex(
                [
                    "No Fatality Reported",
                    "Low",
                    "Moderate",
                    "High",
                    "Extreme",
                    "Unknown",
                ],
                fill_value=0,
            )
            .reset_index()
        )

        impact_counts.columns = [
            "Impact Level",
            "Count",
        ]

        fig = px.bar(
            impact_counts,
            x="Impact Level",
            y="Count",
            title="Historical Impact Distribution",
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    # ========================================================
    # UNIFIED RISK FUSION
    # ========================================================
    st.divider()

    st.markdown(
        '<div class="section-label">'
        "🧠 Unified Risk Fusion"
        "</div>",
        unsafe_allow_html=True,
    )

    if "Final_Risk_Level" in fusion_df.columns:

        risk_series = (
            fusion_df["Final_Risk_Level"]
            .astype(str)
            .str.strip()
            .str.title()
        )

        risk_counts = (
            risk_series
            .value_counts()
            .reindex(
                [
                    "Low",
                    "Moderate",
                    "High",
                    "Critical",
                ],
                fill_value=0,
            )
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Level",
            "Records",
        ]

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Records",
            title="Unified Risk Distribution",
            hole=0.35,
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    # ========================================================
    # HISTORICAL RISK TREND
    # ========================================================
    st.markdown(
        '<div class="section-label">'
        "📈 Historical Risk Trend"
        "</div>",
        unsafe_allow_html=True,
    )

    if "Year" in risk_df.columns:

        yearly_risk = (
            risk_df
            .groupby("Year")
            .size()
            .reset_index(
                name="Risk Records"
            )
        )

        fig = px.line(
            yearly_risk,
            x="Year",
            y="Risk Records",
            markers=True,
            title="Historical Risk Records by Year",
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    # ========================================================
    # ML MODEL INTELLIGENCE
    # ========================================================
    st.divider()

    st.markdown(
        '<div class="section-label">'
        "🤖 ML Model Intelligence"
        "</div>",
        unsafe_allow_html=True,
    )

    if not evaluation_df.empty:

        display_eval = evaluation_df.copy()

        numeric_columns = (
            display_eval
            .select_dtypes(include="number")
            .columns
        )

        for column in numeric_columns:
            display_eval[column] = (
                display_eval[column].round(4)
            )

        st.dataframe(
            display_eval,
            width="stretch",
            hide_index=True,
        )

    # ========================================================
    # DATA SUMMARY
    # ========================================================
    st.divider()

    st.markdown(
        '<div class="section-label">'
        "📚 JEEVAN-NETRA Data Summary"
        "</div>",
        unsafe_allow_html=True,
    )

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            "Flood Inventory Rows",
            f"{len(flood_df):,}",
        )

        st.caption(
            "India Flood Inventory historical records"
        )

    with summary_col2:

        st.metric(
            "Historical Risk Rows",
            f"{len(risk_df):,}",
        )

        st.caption(
            "Rainfall + historical flood risk records"
        )

    with summary_col3:

        st.metric(
            "Risk Fusion Rows",
            f"{len(fusion_df):,}",
        )

        st.caption(
            "Combined risk intelligence records"
        )

    # ========================================================
    # DATA & METHODOLOGY
    # ========================================================
    st.divider()

    with st.expander(
        "🔍 Data & Methodology"
    ):

        st.markdown(
            """
            ### Data Sources

            **Historical Flood Inventory**

            India Flood Inventory v3, covering historical
            flood events across India.

            **Rainfall Intelligence**

            Historical rainfall data from the India
            Meteorological Department dataset.

            **Risk Fusion**

            Rainfall risk signals are combined with
            historical flood presence signals.

            **Machine Learning**

            The historical flood model predicts the
            probability of historical flood presence
            from rainfall-related features.

            ### Important limitation

            These historical datasets support
            **decision intelligence and pattern analysis**.

            They should not be interpreted as a guaranteed
            real-time emergency forecast.

            Missing source fields such as exact event
            coordinates or severity are not fabricated.
            """
        )

    # ========================================================
    # SYSTEM STATUS
    # ========================================================
    st.divider()

    st.success(
        "🟢 JEEVAN-NETRA Analytics Engine Online"
    )

    st.caption(
        "Analytics are generated from the project's "
        "processed datasets and ML evaluation results."
    )

else:

    st.error(
        "Analytics cannot be displayed because the "
        "required datasets could not be loaded."
    )