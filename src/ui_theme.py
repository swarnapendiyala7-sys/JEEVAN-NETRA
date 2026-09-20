import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>

        /* =====================================================
           JEEVAN-NETRA GLOBAL THEME
           ===================================================== */

        /* Main application */
        .stApp {
            background:
                radial-gradient(
                    circle at 5% 5%,
                    rgba(0, 190, 255, 0.13),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 95% 8%,
                    rgba(110, 80, 255, 0.12),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 50% 100%,
                    rgba(0, 220, 180, 0.06),
                    transparent 35%
                ),
                #0b1220;

            color: #edf7ff;
        }


        /* =====================================================
           TOP STREAMLIT HEADER / TOOLBAR
           ===================================================== */

        header[data-testid="stHeader"] {
            background: rgba(11, 18, 32, 0.96) !important;
            border-bottom: 1px solid rgba(70, 190, 255, 0.16);
        }

        header[data-testid="stHeader"] button {
            color: #ccecff !important;
        }

        header[data-testid="stHeader"] button:hover {
            background: rgba(60, 190, 255, 0.10) !important;
        }


        /* Deploy / toolbar area */
        div[data-testid="stToolbar"] {
            background: transparent !important;
        }

        div[data-testid="stToolbar"] button {
            color: #ccecff !important;
        }


        /* =====================================================
           MAIN CONTENT
           ===================================================== */

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #101d31 0%,
                    #0a1424 100%
                );

            border-right: 1px solid rgba(70, 190, 255, 0.18);

            box-shadow:
                8px 0 35px rgba(0, 0, 0, 0.18);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }


        /* Sidebar text */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: #b7c9dc !important;
        }


        /* Sidebar links */
        section[data-testid="stSidebar"] a {
            border-radius: 9px;
            transition:
                background 0.18s ease,
                transform 0.18s ease;
        }

        section[data-testid="stSidebar"] a:hover {
            background: rgba(50, 170, 240, 0.10);
            transform: translateX(3px);
        }


        /* =====================================================
           HEADINGS
           ===================================================== */

        h1 {
            font-weight: 800 !important;

            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #61d8ff,
                    #8c9cff
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h2,
        h3,
        h4 {
            color: #f4faff !important;
            font-weight: 750 !important;
        }

        p {
            color: #b7c9dc;
        }


        /* =====================================================
           METRIC CARDS
           ===================================================== */

        div[data-testid="stMetric"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(24, 46, 74, 0.92),
                    rgba(12, 27, 47, 0.95)
                );

            border: 1px solid rgba(75, 195, 255, 0.20);

            border-radius: 18px;
            padding: 20px;

            box-shadow:
                0 10px 35px rgba(0, 0, 0, 0.18);

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
                0 15px 40px rgba(0, 170, 255, 0.12);
        }

        div[data-testid="stMetricLabel"] {
            color: #91aac2 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #f4fbff !important;
            font-weight: 800 !important;
        }


        /* =====================================================
           ALERTS
           ===================================================== */

        div[data-testid="stAlert"] {
            border-radius: 15px !important;

            background:
                rgba(18, 38, 62, 0.82) !important;

            border:
                1px solid rgba(80, 190, 255, 0.18) !important;

            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.14);
        }


        /* =====================================================
           INPUTS
           ===================================================== */

        input,
        textarea {
            background:
                rgba(14, 29, 48, 0.96) !important;

            color: #f2f9ff !important;

            border:
                1px solid rgba(80, 180, 255, 0.22) !important;

            border-radius: 12px !important;
        }

        input:focus,
        textarea:focus {
            border-color:
                rgba(60, 205, 255, 0.65) !important;

            box-shadow:
                0 0 0 3px rgba(40, 190, 255, 0.08) !important;
        }


        /* =====================================================
           SELECT BOXES
           ===================================================== */

        div[data-baseweb="select"] > div {
            background:
                rgba(14, 29, 48, 0.96) !important;

            border-radius: 12px !important;

            border:
                1px solid rgba(80, 180, 255, 0.22) !important;
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {
            background:
                linear-gradient(
                    135deg,
                    #123858,
                    #10243b
                );

            color: #eaf8ff;

            border:
                1px solid rgba(70, 195, 255, 0.30);

            border-radius: 11px;

            font-weight: 600;

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);

            border-color:
                rgba(80, 210, 255, 0.65);

            box-shadow:
                0 8px 25px rgba(0, 170, 255, 0.13);
        }


        /* =====================================================
           DATAFRAMES
           ===================================================== */

        div[data-testid="stDataFrame"] {
            border:
                1px solid rgba(80, 180, 255, 0.15);

            border-radius: 15px;

            overflow: hidden;
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
                    rgba(70, 190, 255, 0.28),
                    transparent
                );
        }


        /* =====================================================
           SCROLLBAR
           ===================================================== */

        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #0b1220;
        }

        ::-webkit-scrollbar-thumb {
            background:
                linear-gradient(
                    #12618a,
                    #263b72
                );

            border-radius: 10px;
        }


        /* =====================================================
           FOOTER / STREAMLIT UI
           ===================================================== */

        footer {
            background: #0b1220 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )