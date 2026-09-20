import streamlit as st
from pathlib import Path
import sys

# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.vision.image_analyzer import analyze_image
from src.risk_engine import calculate_risk
from src.ui_theme import apply_theme


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="JEEVAN-NETRA | Image Intelligence",
    page_icon="🖼️",
    layout="wide"
)

apply_theme()


# =========================================================
# PAGE-SPECIFIC THEME
# =========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       IMAGE INTELLIGENCE PAGE
    ----------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(0, 180, 255, 0.09),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(120, 70, 255, 0.08),
                transparent 30%
            ),
            #07111f;
    }

    /* Main headings */

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

    /* Upload area */

    section[data-testid="stFileUploaderDropzone"] {
        background: rgba(10, 25, 43, 0.72);
        border: 1px dashed rgba(64, 190, 255, 0.40);
        border-radius: 16px;
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

    /* Progress bars */

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

    /* Dividers */

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

st.title("🖼️ Image Intelligence Center")

st.caption(
    "Computer Vision powered visual risk screening "
    "for community safety and infrastructure monitoring."
)

st.info(
    "👁️ Vision Engine Active • Local CPU-based image screening "
    "with integrated JEEVAN-NETRA risk intelligence"
)

st.divider()


# =========================================================
# ENGINE STATUS
# =========================================================

st.subheader("🧠 Vision Engine")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Vision Engine",
        "Ready"
    )

with col2:
    st.metric(
        "Engine",
        "OpenCV CV"
    )

with col3:
    st.metric(
        "Processing",
        "Local"
    )

with col4:
    st.metric(
        "Supported",
        "JPG / PNG"
    )

st.divider()


# =========================================================
# IMAGE UPLOAD
# =========================================================

st.subheader("📤 Upload Community / Infrastructure Image")

st.caption(
    "Upload a JPG or PNG image for local visual risk screening."
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)


# =========================================================
# IMAGE PROCESSING
# =========================================================

if uploaded_file is not None:

    # =====================================================
    # SAVE TEMPORARY IMAGE
    # =====================================================

    temp_dir = BASE_DIR / "data" / "raw"

    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = temp_dir / "uploaded_image.jpg"

    with open(temp_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    # =====================================================
    # DISPLAY IMAGE
    # =====================================================

    st.subheader("🖼️ Uploaded Image")

    st.image(
        uploaded_file,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    if st.button(
        "🔍 Analyze Image",
        type="primary",
        width="stretch"
    ):

        with st.spinner(
            "Analyzing image with the local vision engine..."
        ):

            try:

                # =================================================
                # OPEN-CV ANALYSIS
                # =================================================

                result = analyze_image(
                    str(temp_path)
                )

                # =================================================
                # SUCCESS MESSAGE
                # =================================================

                st.success(
                    "Image analysis completed successfully."
                )

                st.divider()

                # =================================================
                # MAIN RESULT
                # =================================================

                st.subheader(
                    "🎯 Visual Risk Assessment"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Detected Condition",
                        result["condition"]
                    )

                with col2:
                    st.metric(
                        "Visual Score",
                        f'{result["confidence"]:.1f}%'
                    )

                with col3:
                    st.metric(
                        "Severity",
                        result["severity"]
                    )

                with col4:
                    st.metric(
                        "Risk Level",
                        result["risk_level"]
                    )

                # =================================================
                # RISK ALERT
                # =================================================

                if result["risk_level"] == "CRITICAL":

                    st.error(
                        "🚨 CRITICAL VISUAL RISK DETECTED"
                    )

                elif result["risk_level"] == "HIGH":

                    st.warning(
                        "⚠️ HIGH VISUAL RISK DETECTED"
                    )

                elif result["risk_level"] == "MODERATE":

                    st.warning(
                        "⚠️ MODERATE VISUAL RISK"
                    )

                else:

                    st.info(
                        "ℹ️ LOW VISUAL RISK"
                    )

                # =================================================
                # VISUAL SIGNALS
                # =================================================

                st.divider()

                st.subheader(
                    "📊 Visual Risk Signals"
                )

                scores = result["scores"]

                signal_col1, signal_col2 = st.columns(2)

                with signal_col1:

                    flooding_score = float(
                        scores.get("Flooding", 0)
                    )

                    st.write(
                        f"🌊 **Flooding:** "
                        f"{flooding_score:.2f}%"
                    )

                    st.progress(
                        min(
                            int(flooding_score),
                            100
                        )
                    )

                    road_score = float(
                        scores.get("Road Damage", 0)
                    )

                    st.write(
                        f"🛣️ **Road Damage:** "
                        f"{road_score:.2f}%"
                    )

                    st.progress(
                        min(
                            int(road_score),
                            100
                        )
                    )

                with signal_col2:

                    infrastructure_score = float(
                        scores.get("Infrastructure", 0)
                    )

                    st.write(
                        f"🏗️ **Infrastructure:** "
                        f"{infrastructure_score:.2f}%"
                    )

                    st.progress(
                        min(
                            int(infrastructure_score),
                            100
                        )
                    )

                    obstruction_score = float(
                        scores.get("Obstruction", 0)
                    )

                    st.write(
                        f"🚧 **Obstruction:** "
                        f"{obstruction_score:.2f}%"
                    )

                    st.progress(
                        min(
                            int(obstruction_score),
                            100
                        )
                    )

                # =================================================
                # COMMON RISK ENGINE
                # =================================================

                visual_score = float(
                    result["confidence"]
                )

                integrated_risk = calculate_risk(
                    rainfall=None,
                    historical_flood=None,
                    image=visual_score,
                    report=None,
                    road=float(
                        scores.get(
                            "Road Damage",
                            0
                        )
                    ),
                    infrastructure=float(
                        scores.get(
                            "Infrastructure",
                            0
                        )
                    )
                )

                # =================================================
                # SAVE SESSION SIGNALS
                # =================================================

                st.session_state[
                    "latest_image_risk"
                ] = visual_score

                st.session_state[
                    "latest_road_risk"
                ] = float(
                    scores.get(
                        "Road Damage",
                        0
                    )
                )

                st.session_state[
                    "latest_infrastructure_risk"
                ] = float(
                    scores.get(
                        "Infrastructure",
                        0
                    )
                )

                st.session_state[
                    "latest_image_condition"
                ] = result["condition"]

                st.session_state[
                    "latest_image_risk_level"
                ] = result["risk_level"]

                st.session_state[
                    "latest_integrated_image_risk"
                ] = integrated_risk["final_score"]

                # =================================================
                # INTEGRATED RISK RESULT
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
                        "Image Signal",
                        f"{visual_score:.1f}/100"
                    )

                # =================================================
                # INTEGRATED RISK ALERT
                # =================================================

                if integrated_risk["risk_level"] == "Critical":

                    st.error(
                        "🚨 Common Risk Engine: CRITICAL"
                    )

                elif integrated_risk["risk_level"] == "High":

                    st.warning(
                        "⚠️ Common Risk Engine: HIGH"
                    )

                elif integrated_risk["risk_level"] == "Moderate":

                    st.warning(
                        "⚠️ Common Risk Engine: MODERATE"
                    )

                else:

                    st.success(
                        "🟢 Common Risk Engine: LOW"
                    )

                # =================================================
                # INTEGRATED RECOMMENDATION
                # =================================================

                st.info(
                    integrated_risk[
                        "recommended_action"
                    ]
                )

                # =================================================
                # RISK ENGINE BREAKDOWN
                # =================================================

                with st.expander(
                    "🔗 Integrated Risk Signal Breakdown"
                ):

                    breakdown_col1, breakdown_col2 = st.columns(2)

                    with breakdown_col1:

                        st.write(
                            "**Rainfall:** "
                            f'{integrated_risk["rainfall_risk"]:.2f}/100'
                        )

                        st.write(
                            "**Historical Flood:** "
                            f'{integrated_risk["historical_flood_risk"]:.2f}/100'
                        )

                        st.write(
                            "**Image:** "
                            f'{integrated_risk["image_risk"]:.2f}/100'
                        )

                    with breakdown_col2:

                        st.write(
                            "**Road:** "
                            f'{integrated_risk["road_risk"]:.2f}/100'
                        )

                        st.write(
                            "**Infrastructure:** "
                            f'{integrated_risk["infrastructure_risk"]:.2f}/100'
                        )

                        st.write(
                            "**Community Report:** "
                            f'{integrated_risk["report_risk"]:.2f}/100'
                        )

                # =================================================
                # RECOMMENDED ACTION
                # =================================================

                st.subheader(
                    "🛠️ Recommended Action"
                )

                st.info(
                    result["recommended_action"]
                )

                # =================================================
                # IMAGE INFORMATION
                # =================================================

                with st.expander(
                    "🔎 Image Analysis Details"
                ):

                    detail_col1, detail_col2 = st.columns(2)

                    with detail_col1:

                        st.write(
                            "**Image Width:**",
                            result["image_width"],
                            "pixels"
                        )

                        st.write(
                            "**Image Height:**",
                            result["image_height"],
                            "pixels"
                        )

                        st.write(
                            "**Edge Ratio:**",
                            result["edge_ratio"]
                        )

                    with detail_col2:

                        st.write(
                            "**Water Ratio:**",
                            result["water_ratio"]
                        )

                        st.write(
                            "**Image Contrast:**",
                            result["contrast"]
                        )

                        st.write(
                            "**Detected Contours:**",
                            result["contours"]
                        )

                # =================================================
                # MODEL DISCLAIMER
                # =================================================

                st.divider()

                st.caption(
                    "Note: This is a lightweight OpenCV-based "
                    "visual screening engine. The displayed "
                    "scores are visual indicators, not calibrated "
                    "machine-learning probabilities. The integrated "
                    "risk score is a decision-support signal."
                )

            except Exception as error:

                st.error(
                    "Image analysis failed."
                )

                st.exception(error)


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.info(
        "Upload an image to begin visual risk analysis."
    )

    st.subheader(
        "🔍 Supported Visual Conditions"
    )

    condition_col1, condition_col2 = st.columns(2)

    with condition_col1:

        st.write(
            "🌊 **Flooding**"
        )

        st.caption(
            "Detects visual indicators of water accumulation."
        )

        st.write(
            "🛣️ **Road Damage**"
        )

        st.caption(
            "Identifies visual surface irregularities."
        )

    with condition_col2:

        st.write(
            "🏗️ **Infrastructure**"
        )

        st.caption(
            "Estimates visible structural complexity."
        )

        st.write(
            "🚧 **Obstruction**"
        )

        st.caption(
            "Detects complex or object-heavy areas."
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
    "JEEVAN-NETRA 2.0 • Computer Vision Intelligence Center"
)

st.caption(
    "Images are processed locally. Visual scores are "
    "decision-support indicators, not calibrated probabilities."
)