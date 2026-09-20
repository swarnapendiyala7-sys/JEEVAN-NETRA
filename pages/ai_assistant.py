import sys
from pathlib import Path

import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# =========================================================
# PROJECT MODULES
# =========================================================

from src.ai_rag import JEEVANAI
from src.ui_theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="JEEVAN AI | JEEVAN-NETRA",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# COMMON JEEVAN-NETRA THEME
# Sidebar + Top Toolbar + Global Components
# =========================================================

apply_theme()


# =========================================================
# JEEVAN AI SPECIAL PAGE THEME
# Only the AI content area gets this special styling.
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       AI PAGE BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(0, 210, 255, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(145, 80, 255, 0.11),
                transparent 30%
            ),
            #07101c;
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .block-container {
        max-width: 1450px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       AI TITLE
       ===================================================== */

    .ai-title {
        font-size: 2.4rem;
        font-weight: 850;
        margin-bottom: 5px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #62e5ff,
                #a88cff
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .ai-subtitle {
        color: #91a9bd;
        font-size: 1rem;
        margin-bottom: 25px;
    }


    /* =====================================================
       STATUS CARDS
       ===================================================== */

    .status-box {
        background:
            rgba(10, 35, 55, 0.85);

        border:
            1px solid rgba(70, 210, 255, 0.25);

        border-radius: 14px;
        padding: 15px;
        text-align: center;
    }

    .status-title {
        color: #6ee7ff;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .status-text {
        color: #9bb3c6;
        font-size: 0.75rem;
        margin-top: 5px;
    }


    /* =====================================================
       QUESTION CARD
       ===================================================== */

    .question-card {
        background:
            rgba(12, 29, 48, 0.90);

        border:
            1px solid rgba(70, 190, 255, 0.20);

        border-radius: 18px;
        padding: 22px;
        margin-top: 25px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.18);
    }


    /* =====================================================
       RESPONSE CARD
       ===================================================== */

    .response-card {
        background:
            rgba(8, 38, 48, 0.90);

        border:
            1px solid rgba(0, 220, 190, 0.25);

        border-radius: 18px;
        padding: 20px;
        margin-top: 25px;

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.20);
    }


    /* =====================================================
       AI INPUT
       ===================================================== */

    textarea {
        background:
            #0b1b2c !important;

        color:
            #ffffff !important;

        border:
            1px solid rgba(70, 205, 255, 0.25) !important;

        border-radius:
            14px !important;
    }

    textarea:focus {
        border-color:
            rgba(70, 220, 255, 0.65) !important;

        box-shadow:
            0 0 0 3px rgba(40, 200, 255, 0.08) !important;
    }


    /* =====================================================
       AI BUTTON
       ===================================================== */

    .stButton > button {
        min-height: 48px;

        border-radius: 13px;

        background:
            linear-gradient(
                135deg,
                #075b7a,
                #452a78
            );

        color: white;

        border:
            1px solid rgba(85, 215, 255, 0.40);

        font-weight: 750;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 10px 28px rgba(0, 190, 255, 0.17);
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    div[data-testid="stExpander"] {
        border:
            1px solid rgba(75, 190, 240, 0.17) !important;

        border-radius:
            14px !important;

        background:
            rgba(10, 25, 43, 0.72) !important;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer-line {
        margin-top: 42px;
        padding-top: 18px;

        border-top:
            1px solid rgba(80, 175, 220, 0.14);

        text-align: center;

        color: #71899d;

        font-size: 0.76rem;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="ai-title">🤖 JEEVAN AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ai-subtitle">
        AI-powered community safety intelligence and
        knowledge-based decision support.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SYSTEM STATUS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="status-box">
            <div class="status-title">
                🟢 AI ENGINE
            </div>
            <div class="status-text">
                Ready
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="status-box">
            <div class="status-title">
                🔵 RAG ENGINE
            </div>
            <div class="status-text">
                Knowledge Retrieval Ready
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="status-box">
            <div class="status-title">
                🛡️ SAFETY MODE
            </div>
            <div class="status-text">
                Decision Support
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# AI CAPABILITIES
# =========================================================

st.markdown("### AI Safety Intelligence")

cap1, cap2, cap3, cap4 = st.columns(4)

with cap1:
    st.info(
        "🌊 **Flood Safety**\n\n"
        "Flood awareness and response guidance."
    )

with cap2:
    st.info(
        "⚡ **Electrical Safety**\n\n"
        "Electrical hazard information."
    )

with cap3:
    st.info(
        "🛣️ **Infrastructure**\n\n"
        "Road and infrastructure safety."
    )

with cap4:
    st.info(
        "🚨 **Community Safety**\n\n"
        "Practical risk and response information."
    )


# =========================================================
# LOAD JEEVAN AI
# =========================================================

@st.cache_resource
def load_jeevan_ai():
    return JEEVANAI()


try:

    with st.spinner("Loading JEEVAN AI..."):
        jeevan_ai = load_jeevan_ai()

    st.success("JEEVAN AI is ready.")


    # =====================================================
    # QUESTION AREA
    # =====================================================

    st.markdown(
        '<div class="question-card">',
        unsafe_allow_html=True,
    )

    st.markdown("### 💬 Ask JEEVAN AI")

    st.write(
        "Ask a community safety question. "
        "JEEVAN AI will retrieve relevant knowledge "
        "and generate a response."
    )

    question = st.text_area(
        "Your question",
        placeholder="Example: What should I do during a flood?",
        height=120,
    )

    ask_button = st.button(
        "🤖 Ask JEEVAN AI",
        type="primary",
        width="stretch",
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # =====================================================
    # AI RESPONSE
    # =====================================================

    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a safety question first."
            )

        else:

            with st.spinner(
                "Retrieving knowledge and generating response..."
            ):

                result = jeevan_ai.ask(question)


            st.markdown(
                '<div class="response-card">',
                unsafe_allow_html=True,
            )

            st.markdown("### 🧠 JEEVAN AI Response")

            st.write(result["answer"])

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


            # =================================================
            # SOURCES
            # =================================================

            st.markdown("### 📚 Trusted Knowledge Sources")

            if result["sources"]:

                for index, source in enumerate(
                    result["sources"],
                    start=1,
                ):

                    with st.expander(
                        f"📖 Source {index}: {source['source']}"
                    ):

                        st.write(source["text"])

                        st.caption(
                            "RAG similarity score: "
                            f"{source['score']:.4f}"
                        )

            else:

                st.warning(
                    "No trusted knowledge source was retrieved."
                )


except Exception as error:

    st.error(
        "JEEVAN AI could not be loaded."
    )

    st.write(
        "Please check the project environment and AI dependencies."
    )

    st.exception(error)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "JEEVAN-NETRA 2.0 • AI-Powered Multi-Modal "
    "Community Risk & Response Intelligence"
)

st.caption(
    "AI responses are decision-support information "
    "and should not replace official emergency instructions."
)