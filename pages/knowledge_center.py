import sys
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from rag.retriever import KnowledgeRetriever
from src.ui_theme import apply_theme

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Knowledge Center | JEEVAN-NETRA",
    page_icon="📚",
    layout="wide",
)

# ---------------------------------------------------------
# GLOBAL THEME
# ---------------------------------------------------------
apply_theme()

# ---------------------------------------------------------
# PAGE-SPECIFIC STYLE
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Knowledge Center background */
    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(0, 153, 255, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 15%,
                rgba(125, 70, 255, 0.08),
                transparent 28%
            ),
            #07111f;
    }

    /* Main title */
    .kn-title {
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 0.15rem;
    }

    .kn-subtitle {
        color: #9fb2c8;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    /* Section labels */
    .section-label {
        font-size: 1.15rem;
        font-weight: 750;
        margin-top: 0.4rem;
        margin-bottom: 0.7rem;
    }

    /* Search box */
    div[data-testid="stTextInput"] input {
        background: rgba(9, 24, 42, 0.92);
        border: 1px solid rgba(80, 170, 255, 0.25);
        border-radius: 12px;
        color: #eaf6ff;
        padding: 0.75rem 0.9rem;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(70, 190, 255, 0.75);
        box-shadow: 0 0 0 1px rgba(70, 190, 255, 0.20);
    }

    /* Primary button */
    div.stButton > button[kind="primary"] {
        border-radius: 10px;
        border: 1px solid rgba(72, 183, 255, 0.35);
        background: linear-gradient(
            135deg,
            #087fc1,
            #1769d3
        );
        color: white;
        font-weight: 700;
        transition: 0.2s ease;
    }

    div.stButton > button[kind="primary"]:hover {
        border-color: rgba(100, 220, 255, 0.8);
        transform: translateY(-1px);
        box-shadow: 0 8px 22px rgba(0, 120, 220, 0.18);
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: rgba(8, 23, 40, 0.78);
        border: 1px solid rgba(95, 150, 200, 0.18);
        border-radius: 12px;
        overflow: hidden;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(9, 25, 43, 0.78);
        border: 1px solid rgba(90, 160, 210, 0.16);
        border-radius: 13px;
        padding: 0.85rem 1rem;
    }

    div[data-testid="stMetricLabel"] {
        color: #8fa8bf;
    }

    div[data-testid="stMetricValue"] {
        color: #eaf7ff;
    }

    /* Source pills / code */
    code {
        color: #8ee8ff !important;
    }

    /* Info / success messages */
    div[data-testid="stAlert"] {
        border-radius: 11px;
    }

    /* Divider */
    hr {
        border-color: rgba(100, 160, 210, 0.12);
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="kn-title">📚 JEEVAN-NETRA Knowledge Center</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="kn-subtitle">'
    "Semantic safety knowledge retrieval powered by FAISS Vector RAG."
    "</div>",
    unsafe_allow_html=True,
)

st.info(
    "🧠 RAG Engine Active • Local safety knowledge retrieval • "
    "Semantic search with FAISS"
)

# ---------------------------------------------------------
# INITIALIZE RETRIEVER
# ---------------------------------------------------------
@st.cache_resource
def load_retriever():
    return KnowledgeRetriever(top_k=3)


try:
    retriever = load_retriever()
    engine_status = "🟢 Online"
    engine_error = None
except Exception as error:
    retriever = None
    engine_status = "🔴 Error"
    engine_error = str(error)

    st.error(
        f"Knowledge engine could not be loaded: {error}"
    )

# ---------------------------------------------------------
# ENGINE STATUS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-label">🧠 Knowledge Intelligence Engine</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Knowledge Engine",
        engine_status,
    )

with col2:
    st.metric(
        "Search Type",
        "FAISS Vector RAG",
    )

with col3:
    if retriever is not None:
        st.metric(
            "Knowledge Chunks",
            int(retriever.index.ntotal),
        )
    else:
        st.metric(
            "Knowledge Chunks",
            "—",
        )

with col4:
    st.metric(
        "Retrieval Depth",
        "Top 3",
    )

# ---------------------------------------------------------
# KNOWLEDGE SOURCES
# ---------------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-label">📖 Knowledge Sources</div>',
    unsafe_allow_html=True,
)

source_col1, source_col2, source_col3 = st.columns(3)

with source_col1:
    st.info("🌊 `flood_safety.txt`\n\nFlood and water-safety guidance.")

with source_col2:
    st.info(
        "⚡ `electrical_safety.txt`\n\n"
        "Electrical hazard and safety guidance."
    )

with source_col3:
    st.info(
        "🛣️ `road_safety.txt`\n\n"
        "Road and obstruction safety guidance."
    )

# ---------------------------------------------------------
# SEARCH SECTION
# ---------------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-label">🔎 Ask the Knowledge Center</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Ask a natural-language safety question and JEEVAN-NETRA "
    "will retrieve the most relevant knowledge chunks."
)

question = st.text_input(
    "Knowledge question",
    placeholder="Example: What should I do during a flood?",
    label_visibility="collapsed",
)

search_button = st.button(
    "🔍 Search Knowledge Base",
    type="primary",
    width="stretch",
)

# ---------------------------------------------------------
# SEARCH RESULTS
# ---------------------------------------------------------
if search_button:

    if not question.strip():
        st.warning(
            "Please enter a question before searching."
        )

    elif retriever is None:
        st.error(
            "Knowledge engine is unavailable. "
            "Please check the RAG model and FAISS index."
        )

    else:
        with st.spinner(
            "Searching the JEEVAN-NETRA knowledge base..."
        ):
            try:
                results = retriever.search(question)
            except Exception as error:
                results = []
                st.error(
                    f"Knowledge search failed: {error}"
                )

        if not results:
            st.warning(
                "No relevant knowledge was found for this question."
            )

        else:
            st.success(
                f"Found {len(results)} relevant knowledge chunks."
            )

            st.markdown(
                '<div class="section-label">'
                "🧠 Retrieved Knowledge"
                "</div>",
                unsafe_allow_html=True,
            )

            # -------------------------------------------------
            # DISPLAY RESULTS
            # -------------------------------------------------
            for number, result in enumerate(
                results,
                start=1,
            ):
                score = float(result["score"])
                source = result["source"]
                text = result["text"]

                with st.expander(
                    f"Result {number} — {source}",
                    expanded=(number == 1),
                ):

                    result_col1, result_col2 = st.columns(2)

                    with result_col1:
                        st.write(
                            f"**Source:** `{source}`"
                        )

                    with result_col2:
                        st.write(
                            f"**Similarity:** `{score:.4f}`"
                        )

                    st.progress(
                        max(0.0, min(1.0, score))
                    )

                    st.markdown(
                        "**Relevant Knowledge**"
                    )

                    st.write(text)

            # -------------------------------------------------
            # BEST RESULT
            # -------------------------------------------------
            best_result = results[0]

            st.divider()

            st.markdown(
                '<div class="section-label">'
                "⭐ Most Relevant Knowledge"
                "</div>",
                unsafe_allow_html=True,
            )

            st.info(
                best_result["text"]
            )

            st.caption(
                f"Retrieved from {best_result['source']} "
                f"with similarity score "
                f"{float(best_result['score']):.4f}"
            )

            # -------------------------------------------------
            # RETRIEVAL SUMMARY
            # -------------------------------------------------
            st.markdown(
                "**Retrieval Summary**"
            )

            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:
                st.metric(
                    "Results Retrieved",
                    len(results),
                )

            with summary_col2:
                st.metric(
                    "Best Similarity",
                    f"{float(best_result['score']):.4f}",
                )

            with summary_col3:
                st.metric(
                    "Top Source",
                    str(best_result["source"]),
                )

# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------
st.divider()

with st.expander(
    "ℹ️ How JEEVAN-NETRA RAG works"
):

    st.markdown(
        """
        **1. User Question**

        The user enters a natural-language safety question.

        **2. Embedding**

        The question is converted into a numerical vector
        using `all-MiniLM-L6-v2`.

        **3. FAISS Search**

        FAISS searches the stored knowledge vectors for
        semantically similar knowledge chunks.

        **4. Ranking**

        Retrieved chunks are ranked using similarity scores.

        **5. Knowledge Retrieval**

        JEEVAN-NETRA presents the most relevant safety
        information to support the user's decision.
        """
    )

# ---------------------------------------------------------
# ENGINE INFORMATION
# ---------------------------------------------------------
with st.expander(
    "🔧 Knowledge Engine Information"
):

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.write("**Vector Database:** FAISS")
        st.write("**Embedding Model:** `all-MiniLM-L6-v2`")
        st.write("**Retrieval Strategy:** Semantic similarity")

    with info_col2:
        st.write("**Top-K Results:** 3")
        st.write("**Processing:** Local")
        st.write("**Hardware:** CPU-friendly")

    if engine_error:
        st.error(
            f"Engine error: {engine_error}"
        )

# ---------------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------------
st.divider()

st.caption(
    "JEEVAN-NETRA Knowledge Center uses local safety "
    "documents for retrieval. Retrieved information is "
    "for decision support and should not replace official "
    "emergency instructions."
)

st.caption(
    "JEEVAN-NETRA 2.0 • Knowledge Intelligence Center"
)