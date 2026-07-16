import streamlit as st


def load_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&family=Poppins:wght@600;700&display=swap');

        :root {
            --sage: #789f8b;
            --sage-dark: #557564;
            --sage-light: #e8f3ed;
            --lavender-light: #f3effa;
            --text-main: #344b40;
            --text-muted: #687a71;
            --border: #dce7e1;
            --card: rgba(255, 255, 255, 0.96);
        }

        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    #eef7f2 0%,
                    transparent 32%
                ),
                radial-gradient(
                    circle at top right,
                    #f2edfb 0%,
                    transparent 34%
                ),
                linear-gradient(
                    180deg,
                    #fbfdfc 0%,
                    #f6faf8 100%
                );
        }

        html,
        body,
        [class*="css"] {
            color: var(--text-main);
            font-family: "Nunito", sans-serif;
        }

        h1,
        h2,
        h3 {
            color: var(--text-main);
            font-family: "Poppins", sans-serif;
            letter-spacing: -0.02em;
        }

        .block-container {
            width: 100%;
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        /* ---------------------------------------------------------
           Main cards
        --------------------------------------------------------- */

        .hero,
        .assessment-header {
            margin-bottom: 1.5rem;
            padding: 2.2rem;
            border: 1px solid rgba(131, 164, 148, 0.24);
            border-radius: 26px;
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 18px 45px rgba(88, 113, 101, 0.09);
        }

        .assessment-badge,
        .pill {
            display: inline-block;
            padding: 0.42rem 0.9rem;
            border-radius: 999px;
            background: var(--sage-light);
            color: var(--sage-dark);
            font-size: 0.82rem;
            font-weight: 800;
        }

        .assessment-subtitle {
            max-width: 850px;
            color: var(--text-muted);
            font-size: 1.02rem;
            line-height: 1.75;
        }

        /* ---------------------------------------------------------
           Fixed Version 2 progress bar
        --------------------------------------------------------- */

        .fixed-progress-wrapper {
            position: fixed;
            top: 0.75rem;
            left: calc(50% + 6rem);
            z-index: 9999;
            width: min(900px, calc(100vw - 290px));
            transform: translateX(-50%);
            pointer-events: none;
        }

        .fixed-progress-content {
            padding: 0.9rem 1.1rem;
            border: 1px solid rgba(120, 159, 139, 0.28);
            border-radius: 16px;
            background: rgba(251, 253, 252, 0.97);
            box-shadow: 0 10px 28px rgba(72, 100, 87, 0.14);
            backdrop-filter: blur(14px);
        }

        .fixed-progress-title {
            margin-bottom: 0.55rem;
            color: #52675d;
            font-size: 0.92rem;
            font-weight: 800;
        }

        .fixed-progress-row {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .fixed-progress-track {
            flex: 1;
            height: 10px;
            overflow: hidden;
            border-radius: 999px;
            background: #e9f0ec;
        }

        .fixed-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(
                90deg,
                #7fa58f,
                #8eb09c,
                #a295c2
            );
            transition: width 0.35s ease;
        }

        .fixed-progress-percentage {
            width: 44px;
            flex-shrink: 0;
            color: #52675d;
            font-size: 0.88rem;
            font-weight: 800;
            text-align: right;
        }

        .fixed-progress-count {
            margin-top: 0.45rem;
            color: #7a8c83;
            font-size: 0.76rem;
            font-weight: 700;
        }

        .fixed-progress-spacer {
            height: 5.8rem;
        }

        /* ---------------------------------------------------------
           Question cards
        --------------------------------------------------------- */

        .question-card {
            width: 100%;
            box-sizing: border-box;
            margin-top: 1.35rem;
            padding: 1.35rem 1.5rem 1rem;
            border: 1px solid var(--border);
            border-radius: 22px 22px 0 0;
            background: var(--card);
            box-shadow: 0 8px 22px rgba(88, 113, 101, 0.05);
        }

        .question-card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.9rem;
        }

        .question-number {
            color: #7b8f85;
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .question-category {
            flex-shrink: 0;
            padding: 0.42rem 0.8rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .question-text {
            max-width: 900px;
            color: var(--text-main);
            font-size: 1.08rem;
            font-weight: 700;
            line-height: 1.55;
        }

        /* ---------------------------------------------------------
           Horizontal response options
        --------------------------------------------------------- */

        div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: repeat(4, minmax(155px, 1fr));
            width: 100%;
            box-sizing: border-box;
            gap: 0.8rem;
            margin: 0 0 0.7rem;
            padding: 1.05rem 1.35rem 1.25rem;
            border: 1px solid var(--border);
            border-top: none;
            border-radius: 0 0 22px 22px;
            background: var(--card);
        }

        div[role="radiogroup"] label {
            display: flex !important;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-width: 0;
            min-height: 58px;
            box-sizing: border-box;
            gap: 0.55rem;
            padding: 0.75rem 0.8rem;
            border: 1px solid #d5e2db;
            border-radius: 14px;
            background: #f8fbf9;
            cursor: pointer;
            transition:
                background 0.2s ease,
                border-color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        div[role="radiogroup"] label:hover {
            border-color: #9eb9ac;
            background: #eef6f1;
            transform: translateY(-1px);
        }

        div[role="radiogroup"] label p {
            margin: 0 !important;
            color: #486057;
            font-size: 0.9rem;
            font-weight: 800;
            line-height: 1.25;
            text-align: center;
            white-space: nowrap;
            word-break: normal;
            overflow-wrap: normal;
        }

        div[role="radiogroup"] label[data-baseweb="radio"] {
            overflow: visible;
        }

        div[role="radiogroup"] label:has(input:checked) {
            border-color: #86aa96;
            background: #e6f2eb;
            box-shadow: 0 5px 14px rgba(92, 132, 111, 0.12);
        }

        /* ---------------------------------------------------------
           Result and recommendation cards
        --------------------------------------------------------- */

        .result-card,
        .recommendation-card {
            height: 100%;
            box-sizing: border-box;
            padding: 1.4rem;
            border: 1px solid #e2eae6;
            border-radius: 21px;
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 9px 24px rgba(88, 113, 101, 0.05);
        }

        .result-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.8rem;
        }

        .result-title {
            font-size: 1.2rem;
            font-weight: 800;
        }

        .result-score {
            margin-top: 0.75rem;
            font-size: 3rem;
            font-weight: 800;
            line-height: 1;
        }

        .severity-pill {
            padding: 0.42rem 0.75rem;
            border-radius: 999px;
            color: white;
            font-size: 0.75rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .result-message,
        .recommendation-description {
            margin-top: 0.85rem;
            color: var(--text-muted);
            line-height: 1.65;
        }

        .recommendation-header {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .recommendation-icon {
            font-size: 1.4rem;
        }

        .recommendation-category {
            color: #809189;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .recommendation-title {
            font-size: 1rem;
            font-weight: 800;
        }

        /* ---------------------------------------------------------
           Score bars
        --------------------------------------------------------- */

        .score-bar-card {
            margin-bottom: 1rem;
            padding: 1.05rem 1.15rem;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: white;
        }

        .score-bar-header {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.7rem;
            font-weight: 800;
        }

        .score-bar-track {
            height: 12px;
            overflow: hidden;
            border-radius: 999px;
            background: #edf3f0;
        }

        .score-bar-fill {
            height: 100%;
            border-radius: 999px;
        }

        /* ---------------------------------------------------------
           Safety and insight cards
        --------------------------------------------------------- */

        .safety-card,
        .insight-card {
            margin-top: 1.5rem;
            padding: 1.3rem 1.4rem;
            border-radius: 18px;
        }

        .safety-card {
            border: 1px solid #ead9b5;
            background: #fff9ec;
        }

        .insight-card {
            border: 1px solid #cfe2d7;
            background: #f1f8f4;
        }

        .safety-title,
        .insight-title {
            font-weight: 800;
        }

        .safety-title {
            color: #66593d;
        }

        .insight-title {
            color: #426552;
        }

        .safety-text,
        .insight-text {
            margin-top: 0.45rem;
            line-height: 1.65;
        }

        .safety-text {
            color: #75694c;
        }

        .insight-text {
            color: #597064;
        }

        /* ---------------------------------------------------------
           Buttons
        --------------------------------------------------------- */

        div.stButton > button,
        div.stFormSubmitButton > button {
            min-height: 3rem;
            border: none;
            border-radius: 14px;
            background: var(--sage);
            color: white;
            font-family: "Nunito", sans-serif;
            font-size: 1rem;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(88, 130, 109, 0.16);
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            border: none;
            background: #668b78;
            color: white;
        }

        /* ---------------------------------------------------------
           Tablet
        --------------------------------------------------------- */

        @media (max-width: 900px) {
            .fixed-progress-wrapper {
                left: 50%;
                width: calc(100vw - 2rem);
            }

            div[role="radiogroup"] {
                grid-template-columns: repeat(2, minmax(160px, 1fr));
            }
        }

        /* ---------------------------------------------------------
           Mobile
        --------------------------------------------------------- */

        @media (max-width: 600px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero,
            .assessment-header {
                padding: 1.4rem;
            }

            .question-card-top,
            .result-top,
            .score-bar-header {
                align-items: flex-start;
                flex-direction: column;
            }

            div[role="radiogroup"] {
                grid-template-columns: 1fr;
                padding: 0.9rem;
            }

            div[role="radiogroup"] label p {
                white-space: normal;
            }

            .fixed-progress-wrapper {
                top: 0.4rem;
                width: calc(100vw - 1rem);
            }

            .fixed-progress-content {
                padding: 0.75rem 0.85rem;
            }

            .fixed-progress-title {
                font-size: 0.84rem;
            }

            .fixed-progress-percentage {
                width: 38px;
                font-size: 0.82rem;
            }

            .fixed-progress-count {
                font-size: 0.7rem;
            }

            .fixed-progress-spacer {
                height: 5.4rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )