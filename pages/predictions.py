import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

from src.ui_theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Predictions | JEEVAN-NETRA",
    page_icon="🔮",
    layout="wide"
)

apply_theme()


# ============================================================
# AI PREDICTION INTELLIGENCE THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(0, 190, 255, 0.09),
                transparent 28%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(125, 75, 255, 0.11),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(0, 220, 190, 0.05),
                transparent 35%
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
                rgba(24, 47, 78, 0.95),
                rgba(11, 27, 48, 0.98)
            );

        border:
            1px solid rgba(75, 195, 255, 0.20);

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 10px 32px rgba(0, 0, 0, 0.17);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        border-color:
            rgba(80, 210, 255, 0.58);

        box-shadow:
            0 15px 38px rgba(0, 175, 255, 0.13);
    }


    /* =====================================================
       INPUT CONTROLS
       ===================================================== */

    div[data-baseweb="select"] > div {
        background:
            rgba(13, 29, 49, 0.97) !important;

        border:
            1px solid rgba(75, 190, 250, 0.22) !important;

        border-radius: 12px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color:
            rgba(75, 210, 255, 0.58) !important;

        box-shadow:
            0 0 18px rgba(0, 180, 255, 0.08);
    }


    input {
        background:
            rgba(13, 29, 49, 0.97) !important;
    }


    /* =====================================================
       PREDICTION BUTTON
       ===================================================== */

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #123f62,
                #24336b
            );

        color: #effaff;

        border:
            1px solid rgba(80, 205, 255, 0.32);

        border-radius: 12px;

        font-weight: 700;

        min-height: 46px;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color:
            rgba(90, 220, 255, 0.70);

        box-shadow:
            0 10px 28px rgba(0, 170, 255, 0.16);
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 15px !important;
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
                rgba(75, 195, 255, 0.28),
                transparent
            );
    }


    /* =====================================================
       INFO PANELS
       ===================================================== */

    div[data-testid="stAlert"][data-baseweb="notification"] {
        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.12);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "ml"
    / "historical_flood_model.joblib"
)

PREPROCESSOR_PATH = (
    BASE_DIR
    / "models"
    / "ml"
    / "historical_flood_preprocessor.joblib"
)

EVALUATION_PATH = (
    BASE_DIR
    / "models"
    / "ml"
    / "historical_flood_evaluation.csv"
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    model = joblib.load(
        MODEL_PATH
    )

    preprocessor = joblib.load(
        PREPROCESSOR_PATH
    )

    return model, preprocessor


model, preprocessor = load_model()


# ============================================================
# LOAD MODEL EVALUATION
# ============================================================

evaluation = pd.read_csv(
    EVALUATION_PATH
)

accuracy = evaluation.loc[
    evaluation["Metric"] == "Accuracy",
    "Score"
].iloc[0]

f1_score = evaluation.loc[
    evaluation["Metric"] == "F1 Score",
    "Score"
].iloc[0]


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🔮 Prediction Intelligence Center")

st.caption(
    "AI-powered historical flood prediction using the "
    "trained Random Forest model."
)

st.info(
    "🧠 Prediction Engine Active • "
    "Historical flood intelligence and probability analysis"
)

st.divider()


# ============================================================
# MODEL STATUS
# ============================================================

st.subheader("🧠 Prediction Engine")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Model Status",
        "Ready"
    )

with col2:

    st.metric(
        "Model Type",
        "Random Forest"
    )

with col3:

    st.metric(
        "Accuracy",
        f"{accuracy * 100:.2f}%"
    )

with col4:

    st.metric(
        "F1 Score",
        f"{f1_score * 100:.2f}%"
    )


st.divider()


# ============================================================
# PREDICTION INPUTS
# ============================================================

st.subheader("🔮 Generate Flood Prediction")

st.info(
    "Enter rainfall information to generate a historical "
    "flood prediction."
)


col1, col2 = st.columns(2)


# ============================================================
# LEFT COLUMN
# ============================================================

with col1:

    state = st.selectbox(
        "📍 State",
        [
            "Andhra Pradesh",
            "Telangana",
            "Karnataka",
            "Tamil Nadu",
            "Kerala",
            "Maharashtra",
            "Odisha",
            "West Bengal",
            "Assam",
            "Bihar",
            "Uttar Pradesh",
            "Rajasthan",
            "Gujarat",
            "Madhya Pradesh",
            "Punjab",
            "Haryana",
            "Himachal Pradesh",
            "Uttarakhand",
            "Jammu and Kashmir",
            "Chhattisgarh",
            "Arunachal Pradesh",
            "Goa",
            "Jharkhand"
        ]
    )

    year = st.number_input(
        "📅 Year",
        min_value=1901,
        max_value=2023,
        value=2015,
        step=1
    )

    annual_rainfall = st.number_input(
        "🌧️ Annual Rainfall (mm)",
        min_value=0.0,
        max_value=10000.0,
        value=1000.0,
        step=10.0
    )


# ============================================================
# RIGHT COLUMN
# ============================================================

with col2:

    historical_avg_rainfall = st.number_input(
        "📊 Historical Average Rainfall (mm)",
        min_value=0.0,
        max_value=10000.0,
        value=1000.0,
        step=10.0
    )

    rainfall_anomaly = st.number_input(
        "📈 Rainfall Anomaly (mm)",
        min_value=-10000.0,
        max_value=10000.0,
        value=0.0,
        step=10.0
    )

    rainfall_anomaly_percent = st.number_input(
        "📈 Rainfall Anomaly (%)",
        min_value=-100.0,
        max_value=300.0,
        value=0.0,
        step=1.0
    )

    rainfall_risk_score = st.selectbox(
        "⚠️ Rainfall Risk Score",
        [0, 1, 2, 3],
        format_func=lambda x: {
            0: "0 - Normal",
            1: "1 - Elevated",
            2: "2 - High",
            3: "3 - Extreme"
        }[x]
    )


st.divider()


# ============================================================
# GENERATE PREDICTION
# ============================================================

if st.button(
    "🚀 Generate Prediction",
    width="stretch"
):

    # --------------------------------------------------------
    # CREATE INPUT DATAFRAME
    # --------------------------------------------------------

    input_data = pd.DataFrame([{
        "State": state,
        "Year": year,
        "Annual_Rainfall": annual_rainfall,
        "Historical_Avg_Rainfall":
            historical_avg_rainfall,
        "Rainfall_Anomaly":
            rainfall_anomaly,
        "Rainfall_Anomaly_Percent":
            rainfall_anomaly_percent,
        "Rainfall_Risk_Score":
            rainfall_risk_score
    }])


    # --------------------------------------------------------
    # TRANSFORM INPUT
    # --------------------------------------------------------

    input_processed = preprocessor.transform(
        input_data
    )


    # --------------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------------

    prediction = model.predict(
        input_processed
    )[0]

    probabilities = model.predict_proba(
        input_processed
    )[0]

    flood_probability = probabilities[1] * 100


    # ========================================================
    # RISK LEVEL
    # ========================================================

    if flood_probability >= 75:

        risk_level = "CRITICAL"

    elif flood_probability >= 50:

        risk_level = "HIGH"

    elif flood_probability >= 25:

        risk_level = "MODERATE"

    else:

        risk_level = "LOW"


    # ========================================================
    # RESULT
    # ========================================================

    st.subheader("🎯 Prediction Result")

    col1, col2, col3 = st.columns(3)


    with col1:

        if prediction == 1:

            st.metric(
                "Prediction",
                "🌊 FLOOD"
            )

        else:

            st.metric(
                "Prediction",
                "✅ NO FLOOD"
            )


    with col2:

        st.metric(
            "Flood Probability",
            f"{flood_probability:.2f}%"
        )


    with col3:

        st.metric(
            "Risk Level",
            risk_level
        )


    # ========================================================
    # RISK ALERT
    # ========================================================

    if risk_level == "CRITICAL":

        st.error(
            "🚨 CRITICAL RISK — Immediate monitoring "
            "and emergency preparedness recommended."
        )

    elif risk_level == "HIGH":

        st.warning(
            "⚠️ HIGH RISK — Increased monitoring "
            "and preparedness recommended."
        )

    elif risk_level == "MODERATE":

        st.warning(
            "🟡 MODERATE RISK — Continue monitoring "
            "rainfall and flood conditions."
        )

    else:

        st.success(
            "✅ LOW RISK — No strong historical flood "
            "signal detected by the model."
        )


st.divider()


# ============================================================
# MODEL INFORMATION
# ============================================================

st.subheader("📈 Model Information")

info_col1, info_col2 = st.columns(2)

with info_col1:

    st.write(
        "**Algorithm:** Random Forest"
    )

    st.write(
        f"**Accuracy:** {accuracy * 100:.2f}%"
    )


with info_col2:

    st.write(
        f"**F1 Score:** {f1_score * 100:.2f}%"
    )

    st.write(
        "**Target:** Historical Flood Presence"
    )


st.divider()


# ============================================================
# PREDICTION PIPELINE
# ============================================================

st.subheader("📋 Prediction Pipeline")

st.info(
    "Rainfall Data → Preprocessing → Random Forest "
    "Model → Flood Probability → Risk Level"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "JEEVAN-NETRA 2.0 • AI Prediction Intelligence Center"
)

st.caption(
    "Model output is historical-data-based decision support "
    "and does not guarantee a future flood event."
)