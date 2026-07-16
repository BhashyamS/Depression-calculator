import streamlit as st


st.set_page_config(
    page_title="MindSense",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


pages = {
    "MindSense": [
        st.Page(
            "pages/home.py",
            title="Home",
            icon=":material/home:",
            default=True,
        ),
    ],

    "Assessment Versions": [
        st.Page(
            "pages/version_1.py",
            title="Classic — Version 1",
            icon=":material/checklist:",
        ),

        st.Page(
            "pages/version_2.py",
            title="Enhanced — Version 2",
            icon=":material/auto_awesome:",
        ),

        st.Page(
            "pages/version_3.py",
            title="Tracker — Version 3",
            icon=":material/monitoring:",
        ),

        st.Page("pages/version_4_ml.py", title="ML Insights — Version 4", icon=":material/model_training:"),
    ],

    "Information": [
        st.Page(
            "pages/about.py",
            title="About DASS-21",
            icon=":material/info:",
        ),

        st.Page(
            "pages/resources.py",
            title="Support Resources",
            icon=":material/favorite:",
        ),
    ],
}


navigation = st.navigation(
    pages,
    position="sidebar",
)

navigation.run()