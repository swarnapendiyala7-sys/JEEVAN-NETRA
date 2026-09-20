import streamlit as st
from pathlib import Path
import sys

# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.nlp.report_analyzer import analyze_report
from src.risk_engine import calculate_risk
from src.ui_theme import apply_theme


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="JEEVAN-NETRA | Report Analyzer",
    page_icon="📝",
    layout="wide"
)

apply_theme()


# =========================================================
# PAGE-SPECIFIC THEME
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 15% 8%,
                rgba(0, 190, 255, 0.09),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 18%,
                rgba(120, 70, 255, 0.09),
                transparent 30%
            ),
            #07111f;
    }

    h1 {
        letter-spacing: -0.8px;
    }

    h2, h3 {
        letter-spacing: -0.3px;
    }

    /* Metric cards */

    div[data-testid="stMetric"] {
        background: linear-gradient(
            135deg,
            rgba(15, 31, 53, 0.96),
            rgba(9, 23, 41, 0.96)
        );
        border: 1px solid rgba(74, 180, 255, 0.18);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.20);
        transition: all 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(74, 200, 255, 0.42);
        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] {
        color: #9fb4cc !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f4f8ff !important;
    }

    /* Report input */

    textarea {
        background: rgba(8, 23, 40, 0.82) !important;
        border: 1px solid rgba(70, 180, 255, 0.20) !important;
        border-radius: 14px !important;
    }

    textarea:focus {
        border-color: rgba(70, 200, 255, 0.55) !important;
        box-shadow: 0 0 0 1px rgba(70, 200, 255, 0.18) !important;
    }

    /* Primary button */

    div.stButton > button[kind="primary"] {
        background: linear-gradient(
            90deg,
            #087fca,
            #2256d8,
            #7048d8
        );
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        min-height: 46px;
        box-shadow: 0 8px 22px rgba(20, 120, 220, 0.20);
    }

    div.stButton > button[kind="primary"]:hover {
        border: none;
        color: white;
        filter: brightness(1.10);
    }

    /* Progress */

    div[data-testid="stProgressBar"] > div {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
    }

    /* Expanders */

    div[data-testid="stExpander"] {
        background: rgba(10, 25, 43, 0.55);
        border: 1px solid rgba(90, 160, 220, 0.16);
        border-radius: 14px;
    }

    /* Alerts */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: rgba(120, 170, 220, 0.12);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.title("📝 Community Report Intelligence")

st.caption(
    "NLP-powered community report analysis for incident "
    "identification, severity assessment and risk prioritization."
)

st.info(
    "🧠 NLP Engine Active • Local report screening with "
    "JEEVAN-NETRA Common Risk Engine integration"
)

st.divider()


# =========================================================
# ENGINE STATUS
# =========================================================

st.subheader("🧠 NLP Intelligence Engine")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("NLP Engine", "Ready")

with col2:
    st.metric("Processing", "Local")

with col3:
    st.metric("Analysis", "Rule-Based NLP")

with col4:
    st.metric("Risk Engine", "Connected")

st.divider()


# =========================================================
# REPORT INPUT
# =========================================================

st.subheader("📝 Enter Community Report")

st.caption(
    "Describe the incident, location or community problem "
    "in natural language."
)

report_text = st.text_area(
    "Community report",
    placeholder=(
        "Example: Heavy rain caused flooding on the road. "
        "Water is entering nearby houses and the road is blocked."
    ),
    height=180
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze Report",
    type="primary",
    width="stretch"
):

    if not report_text.strip():

        st.warning(
            "Please enter a report before analyzing."
        )

    else:

        with st.spinner("Analyzing community report..."):

            try:

                # =================================================
                # NLP ANALYSIS
                # =================================================

                result = analyze_report(
                    report_text
                )

                st.success(
                    "Report analysis completed successfully."
                )

                st.divider()

                # =================================================
                # MAIN ASSESSMENT
                # =================================================

                st.subheader(
                    "🎯 Report Risk Assessment"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Incident",
                        result["incident"]
                    )

                with col2:
                    st.metric(
                        "Location",
                        result["location"]
                    )

                with col3:
                    st.metric(
                        "Severity",
                        result["severity"]
                    )

                with col4:
                    st.metric(
                        "NLP Risk Level",
                        result["risk_level"]
                    )

                # =================================================
                # COMMON RISK ENGINE
                # =================================================

                report_score = float(
                    result["risk_score"]
                )

                road_signal = 0.0
                infrastructure_signal = 0.0

                incident_name = str(
                    result.get("incident", "")
                ).lower()

                detected_incidents = [
                    str(item).lower()
                    for item in result.get(
                        "detected_incidents",
                        []
                    )
                ]

                all_incidents = (
                    " ".join(detected_incidents)
                    + " "
                    + incident_name
                )

                if (
                    "road" in all_incidents
                    or "pothole" in report_text.lower()
                    or "blocked road" in report_text.lower()
                ):
                    road_signal = report_score

                if (
                    "infrastructure" in all_incidents
                    or "building" in report_text.lower()
                    or "bridge" in report_text.lower()
                    or "collapsed" in report_text.lower()
                ):
                    infrastructure_signal = report_score

                integrated_risk = calculate_risk(
                    rainfall=None,
                    historical_flood=None,
                    image=None,
                    report=report_score,
                    road=(
                        road_signal
                        if road_signal > 0
                        else None
                    ),
                    infrastructure=(
                        infrastructure_signal
                        if infrastructure_signal > 0
                        else None
                    )
                )

                # =================================================
                # SAVE SESSION SIGNALS
                # =================================================

                st.session_state[
                    "latest_report_risk"
                ] = report_score

                st.session_state[
                    "latest_report_incident"
                ] = result["incident"]

                st.session_state[
                    "latest_report_location"
                ] = result["location"]

                st.session_state[
                    "latest_report_risk_level"
                ] = result["risk_level"]

                st.session_state[
                    "latest_integrated_report_risk"
                ] = integrated_risk["final_score"]

                # =================================================
                # NLP RISK SCORE
                # =================================================

                st.divider()

                st.subheader(
                    "📊 NLP Risk Score"
                )

                st.progress(
                    min(
                        max(
                            int(report_score),
                            0
                        ),
                        100
                    )
                )

                st.write(
                    f"**NLP Risk Score: "
                    f"{report_score:.1f}/100**"
                )

                # =================================================
                # INTEGRATED RISK
                # =================================================

                st.divider()

                st.subheader(
                    "🔗 JEEVAN-NETRA Integrated Risk"
                )

                risk_col1, risk_col2, risk_col3 = st.columns(3)

                with risk_col1:

                    st.metric(
                        "Integrated Score",
                        f'{integrated_risk["final_score"]:.2f}/100'
                    )

                with risk_col2:

                    st.metric(
                        "Integrated Risk",
                        integrated_risk["risk_level"]
                    )

                with risk_col3:

                    st.metric(
                        "Community Report Signal",
                        f"{report_score:.1f}/100"
                    )

                # =================================================
                # INTEGRATED RISK ALERT
                # =================================================

                integrated_level = (
                    integrated_risk["risk_level"]
                )

                if integrated_level == "Critical":

                    st.error(
                        "🚨 Common Risk Engine: CRITICAL"
                    )

                elif integrated_level == "High":

                    st.warning(
                        "⚠️ Common Risk Engine: HIGH"
                    )

                elif integrated_level == "Moderate":

                    st.warning(
                        "⚠️ Common Risk Engine: MODERATE"
                    )

                else:

                    st.info(
                        "ℹ️ Common Risk Engine: LOW"
                    )

                # =================================================
                # INTEGRATED SIGNAL BREAKDOWN
                # =================================================

                with st.expander(
                    "🔗 Integrated Risk Signal Breakdown",
                    expanded=True
                ):

                    signal1, signal2, signal3 = st.columns(3)

                    with signal1:

                        st.write(
                            "**Rainfall:** "
                            f'{integrated_risk["rainfall_risk"]:.2f}/100'
                        )

                        st.write(
                            "**Historical Flood:** "
                            f'{integrated_risk["historical_flood_risk"]:.2f}/100'
                        )

                    with signal2:

                        st.write(
                            "**Image:** "
                            f'{integrated_risk["image_risk"]:.2f}/100'
                        )

                        st.write(
                            "**Community Report:** "
                            f'{integrated_risk["report_risk"]:.2f}/100'
                        )

                    with signal3:

                        st.write(
                            "**Road:** "
                            f'{integrated_risk["road_risk"]:.2f}/100'
                        )

                        st.write(
                            "**Infrastructure:** "
                            f'{integrated_risk["infrastructure_risk"]:.2f}/100'
                        )

                # =================================================
                # INTEGRATED RECOMMENDATION
                # =================================================

                st.subheader(
                    "🛠️ Integrated Recommended Action"
                )

                st.info(
                    integrated_risk["recommended_action"]
                )

                # =================================================
                # NLP RISK ALERT
                # =================================================

                st.subheader(
                    "🚨 NLP Risk Assessment"
                )

                if result["risk_level"] == "CRITICAL":

                    st.error(
                        "🚨 CRITICAL RISK DETECTED"
                    )

                elif result["risk_level"] == "HIGH":

                    st.warning(
                        "⚠️ HIGH RISK DETECTED"
                    )

                elif result["risk_level"] == "MODERATE":

                    st.warning(
                        "⚠️ MODERATE RISK DETECTED"
                    )

                else:

                    st.info(
                        "ℹ️ LOW RISK"
                    )

                # =================================================
                # DETECTED INCIDENTS
                # =================================================

                st.subheader(
                    "🚨 Detected Incidents"
                )

                detected_incidents = result[
                    "detected_incidents"
                ]

                if detected_incidents:

                    for incident in detected_incidents:

                        st.write(
                            f"• **{incident}**"
                        )

                else:

                    st.write(
                        "No known incident type detected."
                    )

                # =================================================
                # RISK KEYWORDS
                # =================================================

                st.subheader(
                    "🔑 Risk Keywords"
                )

                risk_keywords = result[
                    "risk_keywords"
                ]

                if risk_keywords:

                    st.write(
                        ", ".join(
                            f"**{word}**"
                            for word in risk_keywords
                        )
                    )

                else:

                    st.write(
                        "No high-risk keywords detected."
                    )

                # =================================================
                # NLP RECOMMENDED ACTION
                # =================================================

                st.subheader(
                    "🛠️ NLP Recommended Action"
                )

                st.info(
                    result["recommended_action"]
                )

                # =================================================
                # DETECTION DETAILS
                # =================================================

                with st.expander(
                    "🔎 Detection Details"
                ):

                    matched_keywords = result[
                        "matched_keywords"
                    ]

                    if matched_keywords:

                        for incident, keywords in (
                            matched_keywords.items()
                        ):

                            st.write(
                                f"**{incident}:** "
                                + ", ".join(keywords)
                            )

                    else:

                        st.write(
                            "No incident keywords matched."
                        )

                # =================================================
                # REPORT INFORMATION
                # =================================================

                with st.expander(
                    "📄 Report Information"
                ):

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:

                        st.write(
                            "**Character Count:**",
                            result["report_length"]
                        )

                    with info_col2:

                        st.write(
                            "**Word Count:**",
                            result["word_count"]
                        )

                # =================================================
                # PIPELINE
                # =================================================

                st.subheader(
                    "🔄 Analysis Pipeline"
                )

                st.info(
                    "Report → Keyword Detection → "
                    "Incident Identification → Location Extraction → "
                    "Severity Assessment → Risk Score → "
                    "Common Risk Engine → Recommended Action"
                )

                # =================================================
                # DISCLAIMER
                # =================================================

                st.divider()

                st.caption(
                    "Note: This is a lightweight rule-based NLP "
                    "screening engine. It is intended as a "
                    "decision-support component and does not replace "
                    "official emergency assessment or human review. "
                    "The integrated risk score combines available "
                    "signals using the JEEVAN-NETRA Common Risk Engine."
                )

            except Exception as error:

                st.error(
                    "Report analysis failed."
                )

                st.exception(error)


# =========================================================
# EMPTY STATE
# =========================================================

if not report_text:

    st.info(
        "Enter a community report above and click "
        "'Analyze Report' to begin."
    )

    st.subheader(
        "🔍 What JEEVAN-NETRA Can Detect"
    )

    condition_col1, condition_col2 = st.columns(2)

    with condition_col1:

        st.write(
            "🌊 **Flooding**"
        )

        st.caption(
            "Heavy rain, flooding, waterlogging and overflow."
        )

        st.write(
            "🛣️ **Road Damage**"
        )

        st.caption(
            "Potholes, damaged roads and road problems."
        )

        st.write(
            "⚡ **Electrical Hazards**"
        )

        st.caption(
            "Electrical shocks, sparking, short circuits "
            "and power-line problems."
        )

    with condition_col2:

        st.write(
            "🔥 **Fire**"
        )

        st.caption(
            "Fire, smoke, flames and burning incidents."
        )

        st.write(
            "🏗️ **Infrastructure Damage**"
        )

        st.caption(
            "Collapsed structures, damaged buildings and bridges."
        )

        st.write(
            "🚧 **Obstructions**"
        )

        st.caption(
            "Garbage, debris, blocked roads and other obstructions."
        )

    st.divider()

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.metric(
            "Processing",
            "Local"
        )

    with info_col2:
        st.metric(
            "Hardware",
            "CPU-friendly"
        )

    with info_col3:
        st.metric(
            "Privacy",
            "Local Processing"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "JEEVAN-NETRA 2.0 • Community Report Intelligence Center"
)

st.caption(
    "NLP outputs are decision-support signals and should "
    "be reviewed alongside official information."
)