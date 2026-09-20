import streamlit as st
from pathlib import Path

from src.ui_theme import apply_theme


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Settings | JEEVAN-NETRA",
    page_icon="⚙️",
    layout="wide"
)

apply_theme()


# ============================================================
# PAGE-SPECIFIC STYLE
# ============================================================

st.markdown(
    """
    <style>
    .settings-header {
        padding: 10px 0 18px 0;
    }

    .settings-header h1 {
        margin-bottom: 6px;
    }

    .settings-subtitle {
        color: #9fb3c8;
        font-size: 1.02rem;
        margin-bottom: 8px;
    }

    .settings-section {
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .status-card {
        padding: 4px;
    }

    div[data-testid="stMetric"] {
        background: rgba(17, 31, 52, 0.72);
        border: 1px solid rgba(72, 156, 255, 0.18);
        border-radius: 14px;
        padding: 14px;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(72, 190, 255, 0.42);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(72, 156, 255, 0.18);
        border-radius: 14px;
        background: rgba(12, 24, 42, 0.55);
    }

    .settings-note {
        color: #a9bbcf;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="settings-header">
        <h1>⚙️ JEEVAN-NETRA Settings</h1>
        <div class="settings-subtitle">
            Platform Configuration Center • Application preferences,
            AI configuration, alerts, privacy and system information.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SYSTEM STATUS
# ============================================================

st.subheader("🟢 System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Platform", "Online")

with col2:
    st.metric("AI Engine", "Ready")

with col3:
    st.metric("Risk Engine", "Ready")

with col4:
    st.metric("RAG Engine", "Ready")


st.divider()


# ============================================================
# DISPLAY SETTINGS
# ============================================================

st.subheader("🎨 Display Settings")

col1, col2 = st.columns(2)

with col1:
    dashboard_mode = st.selectbox(
        "Dashboard Mode",
        [
            "Standard",
            "Compact",
            "Detailed"
        ],
        key="dashboard_mode"
    )

with col2:
    refresh_interval = st.selectbox(
        "Data Refresh Interval",
        [
            "Manual",
            "5 minutes",
            "15 minutes",
            "30 minutes"
        ],
        key="refresh_interval"
    )


st.divider()


# ============================================================
# AI SETTINGS
# ============================================================

st.subheader("🤖 AI Configuration")

col1, col2 = st.columns(2)

with col1:
    ai_assistant = st.toggle(
        "Enable JEEVAN AI Assistant",
        value=True,
        key="ai_assistant"
    )

with col2:
    rag_enabled = st.toggle(
        "Enable Knowledge Retrieval",
        value=True,
        key="rag_enabled"
    )

st.info(
    "JEEVAN AI uses the project's local knowledge base "
    "and safety-focused response system."
)


st.divider()


# ============================================================
# ALERT SETTINGS
# ============================================================

st.subheader("🚨 Alert Configuration")

col1, col2 = st.columns(2)

with col1:
    critical_alerts = st.toggle(
        "Critical Risk Alerts",
        value=True,
        key="critical_alerts"
    )

with col2:
    high_alerts = st.toggle(
        "High Risk Alerts",
        value=True,
        key="high_alerts"
    )


st.divider()


# ============================================================
# PRIVACY & SAFETY
# ============================================================

st.subheader("🔐 Privacy & Safety")

privacy_mode = st.selectbox(
    "Privacy Mode",
    [
        "Standard",
        "Enhanced Privacy"
    ],
    key="privacy_mode"
)

st.checkbox(
    "Do not store uploaded images permanently",
    value=True,
    key="no_image_storage"
)

st.checkbox(
    "Do not store community reports permanently",
    value=True,
    key="no_report_storage"
)

st.warning(
    "JEEVAN-NETRA is a decision-support platform. "
    "Its predictions and risk indicators should not be treated "
    "as guaranteed emergency forecasts."
)


st.divider()


# ============================================================
# DATA INFORMATION
# ============================================================

st.subheader("📊 Data Configuration")

BASE_DIR = Path(__file__).resolve().parents[1]
data_dir = BASE_DIR / "data"

if data_dir.exists():
    st.success("🟢 Project data directory detected")
else:
    st.error("🔴 Project data directory not found")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Data Directory",
        "Available" if data_dir.exists() else "Missing"
    )

with col2:
    st.metric(
        "Project Storage",
        "Local"
    )

with col3:
    st.metric(
        "Database",
        "Configured"
    )


st.divider()


# ============================================================
# APPLICATION INFORMATION
# ============================================================

st.subheader("ℹ️ Application Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown(
        """
        **Application**

        **JEEVAN-NETRA 2.0**

        AI-Powered Multi-Modal Community Risk &  
        Response Intelligence Platform
        """
    )

with info_col2:
    st.markdown(
        """
        **Technology Stack**

        - Python
        - Streamlit
        - Machine Learning
        - Computer Vision
        - NLP
        - FAISS RAG
        - Generative AI
        - Pandas
        - Plotly
        """
    )


st.divider()


# ============================================================
# SAVE SETTINGS
# ============================================================

if st.button(
    "💾 Save Settings",
    type="primary",
    width="stretch"
):
    st.success(
        "✅ Settings saved successfully for this session."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "JEEVAN-NETRA 2.0 • Community Risk & Response Intelligence"
)