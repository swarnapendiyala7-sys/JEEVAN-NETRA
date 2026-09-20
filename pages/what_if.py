import streamlit as st

from src.ui_theme import apply_theme


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="What-If Simulator | JEEVAN-NETRA",
    page_icon="🧪",
    layout="wide",
)

apply_theme()


# ---------------------------------------------------------
# PAGE-SPECIFIC STYLE
# ---------------------------------------------------------
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
                circle at 88% 12%,
                rgba(125, 70, 255, 0.08),
                transparent 28%
            ),
            #07111f;
    }

    .sim-title {
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 0.15rem;
    }

    .sim-subtitle {
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

    div[data-testid="stSlider"] {
        background: rgba(8, 23, 40, 0.45);
        border-radius: 12px;
        padding: 0.55rem 0.8rem 0.25rem 0.8rem;
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


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="sim-title">🧪 What-If Risk Simulator</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sim-subtitle">'
    "Explore how changing environmental, infrastructure and "
    "intelligence signals can affect simulated community risk."
    "</div>",
    unsafe_allow_html=True,
)

st.info(
    "🧪 Simulation Engine Active • Adjust the signals below "
    "to explore different community-risk scenarios."
)


# ---------------------------------------------------------
# ENVIRONMENTAL CONDITIONS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-label">🌧️ Environmental Conditions</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    rainfall = st.slider(
        "Rainfall intensity",
        min_value=0,
        max_value=200,
        value=50,
        step=5,
        help="Simulated rainfall intensity.",
    )

with col2:
    flood_history = st.slider(
        "Historical flood signal",
        min_value=0,
        max_value=100,
        value=20,
        step=5,
        help="Strength of historical flood evidence.",
    )


# ---------------------------------------------------------
# INFRASTRUCTURE CONDITIONS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-label">🏗️ Infrastructure Conditions</div>',
    unsafe_allow_html=True,
)

col3, col4 = st.columns(2)

with col3:
    road_damage = st.slider(
        "Road damage",
        min_value=0,
        max_value=100,
        value=10,
        step=5,
        help="Simulated road damage signal.",
    )

with col4:
    infrastructure_damage = st.slider(
        "Infrastructure damage",
        min_value=0,
        max_value=100,
        value=10,
        step=5,
        help="Simulated infrastructure damage signal.",
    )


# ---------------------------------------------------------
# INTELLIGENCE SIGNALS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-label">📡 Intelligence Signals</div>',
    unsafe_allow_html=True,
)

col5, col6 = st.columns(2)

with col5:
    image_risk = st.slider(
        "Image risk signal",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        help="Simulated computer-vision risk signal.",
    )

with col6:
    report_risk = st.slider(
        "Community report risk",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        help="Simulated NLP/community-report risk signal.",
    )


# ---------------------------------------------------------
# RISK CALCULATION
# ---------------------------------------------------------
rainfall_score = min(rainfall / 200 * 100, 100)
historical_score = flood_history
road_score = road_damage
infrastructure_score = infrastructure_damage
image_score = image_risk
report_score = report_risk

overall_score = (
    rainfall_score * 0.25
    + historical_score * 0.20
    + road_score * 0.15
    + infrastructure_score * 0.15
    + image_score * 0.15
    + report_score * 0.10
)


# ---------------------------------------------------------
# RISK LEVEL
# ---------------------------------------------------------
if overall_score >= 75:
    risk_level = "CRITICAL"
    action = (
        "Immediate response required. Inspect the affected "
        "area and activate appropriate emergency procedures."
    )
elif overall_score >= 50:
    risk_level = "HIGH"
    action = (
        "High risk detected. Increase monitoring and "
        "inspect vulnerable infrastructure."
    )
elif overall_score >= 25:
    risk_level = "MODERATE"
    action = (
        "Moderate risk detected. Continue monitoring "
        "environmental and infrastructure conditions."
    )
else:
    risk_level = "LOW"
    action = (
        "Current simulated conditions indicate relatively "
        "low community risk."
    )


# ---------------------------------------------------------
# SIMULATION RESULT
# ---------------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-label">🎯 Simulation Result</div>',
    unsafe_allow_html=True,
)

result_col1, result_col2, result_col3 = st.columns(3)

with result_col1:
    st.metric(
        "Overall Risk Score",
        f"{overall_score:.1f}/100",
    )

with result_col2:
    st.metric(
        "Risk Level",
        risk_level,
    )

with result_col3:
    st.metric(
        "Rainfall Signal",
        f"{rainfall_score:.1f}/100",
    )


if risk_level == "CRITICAL":
    st.error(f"🚨 {risk_level} RISK")

elif risk_level == "HIGH":
    st.warning(f"⚠️ {risk_level} RISK")

elif risk_level == "MODERATE":
    st.info(f"🟠 {risk_level} RISK")

else:
    st.success(f"🟢 {risk_level} RISK")


st.markdown("### 🛠️ Recommended Action")
st.write(action)


# ---------------------------------------------------------
# SIGNAL BREAKDOWN
# ---------------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-label">📊 Risk Signal Breakdown</div>',
    unsafe_allow_html=True,
)

signals = {
    "Rainfall": rainfall_score,
    "Historical Flood": historical_score,
    "Road Damage": road_score,
    "Infrastructure Damage": infrastructure_score,
    "Image Intelligence": image_score,
    "Community Reports": report_score,
}

for signal_name, signal_value in signals.items():

    st.write(
        f"**{signal_name}:** {signal_value:.1f}/100"
    )

    st.progress(
        int(max(0, min(100, signal_value)))
    )


# ---------------------------------------------------------
# SCENARIO INTERPRETATION
# ---------------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-label">🧠 Scenario Interpretation</div>',
    unsafe_allow_html=True,
)

interpretations = []

if rainfall >= 150:
    interpretations.append(
        "🌧️ Very high rainfall is contributing strongly "
        "to the simulated risk."
    )

if flood_history >= 70:
    interpretations.append(
        "🌊 Strong historical flood evidence is increasing "
        "the simulated risk."
    )

if road_damage >= 60:
    interpretations.append(
        "🚧 Significant road damage may increase "
        "accessibility and safety concerns."
    )

if infrastructure_damage >= 60:
    interpretations.append(
        "🏗️ Significant infrastructure damage is increasing "
        "the simulated risk."
    )

if image_risk >= 60:
    interpretations.append(
        "📷 Image intelligence indicates a significant "
        "visual risk signal."
    )

if report_risk >= 60:
    interpretations.append(
        "📝 Community reports indicate a significant "
        "reported-risk signal."
    )

if not interpretations:
    interpretations.append(
        "No individual signal is currently dominating "
        "the simulation."
    )

for interpretation in interpretations:
    st.write(interpretation)


# ---------------------------------------------------------
# WEIGHT CONFIGURATION
# ---------------------------------------------------------
st.divider()

with st.expander("⚖️ Risk Signal Weights"):

    weight_col1, weight_col2, weight_col3 = st.columns(3)

    with weight_col1:
        st.metric("Rainfall", "25%")
        st.metric("Historical Flood", "20%")

    with weight_col2:
        st.metric("Road Damage", "15%")
        st.metric("Infrastructure", "15%")

    with weight_col3:
        st.metric("Image Intelligence", "15%")
        st.metric("Community Reports", "10%")


# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------
with st.expander("🧠 How the What-If Simulator Works"):

    st.markdown(
        """
        The simulator combines six independent risk signals.

        **Rainfall → 25%**

        **Historical Flood Signal → 20%**

        **Road Damage → 15%**

        **Infrastructure Damage → 15%**

        **Image Intelligence → 15%**

        **Community Reports → 10%**

        These signals are combined into an overall simulated
        risk score from **0 to 100**.

        The score is classified into:

        - 🟢 Low
        - 🟠 Moderate
        - 🟡 High
        - 🔴 Critical

        This is a **decision-support simulation**, not an
        official emergency prediction.
        """
    )


# ---------------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------------
st.divider()

st.caption(
    "JEEVAN-NETRA What-If Simulator is designed for "
    "scenario exploration and decision support. "
    "Simulated results should not be treated as official "
    "emergency predictions."
)

st.caption(
    "JEEVAN-NETRA 2.0 • What-If Risk Simulation Center"
)