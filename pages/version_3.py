import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.layout.footer import render_footer
from components.ui.styles import load_styles


load_styles()

st.title("Wellness Tracker — Version 3")

st.info(
    "Prototype preview: this version demonstrates how recurring "
    "weekly assessments and progress tracking could work."
)

history = pd.DataFrame(
    {
        "Week": [
            "Week 1",
            "Week 2",
            "Week 3",
            "Week 4",
        ],
        "Depression": [18, 16, 14, 12],
        "Anxiety": [14, 15, 12, 10],
        "Stress": [22, 20, 18, 16],
    }
)

figure = go.Figure()

chart_settings = {
    "Depression": {
        "color": "#8DBBE8",
        "symbol": "circle",
    },
    "Anxiety": {
        "color": "#718EC8",
        "symbol": "circle",
    },
    "Stress": {
        "color": "#D98C7C",
        "symbol": "circle",
    },
}

for scale, settings in chart_settings.items():
    figure.add_trace(
        go.Scatter(
            x=history["Week"],
            y=history[scale],
            mode="lines+markers",
            name=scale,
            line={
                "color": settings["color"],
                "width": 3,
                "shape": "spline",
            },
            marker={
                "color": settings["color"],
                "size": 8,
                "symbol": settings["symbol"],
            },
            hovertemplate=(
                f"<b>{scale}</b><br>"
                "Week: %{x}<br>"
                "Score: %{y}"
                "<extra></extra>"
            ),
        )
    )

figure.update_layout(
    height=430,
    margin={
        "l": 25,
        "r": 25,
        "t": 30,
        "b": 25,
    },
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.72)",
    hovermode="x unified",
    legend={
        "orientation": "h",
        "yanchor": "bottom",
        "y": -0.22,
        "xanchor": "center",
        "x": 0.5,
    },
    xaxis={
        "title": None,
        "showgrid": False,
        "linecolor": "#DDE7E2",
    },
    yaxis={
        "title": "DASS-21 score",
        "range": [0, 25],
        "gridcolor": "#E4ECE8",
        "zeroline": False,
    },
    font={
        "family": "Nunito",
        "color": "#53675D",
    },
)

st.plotly_chart(
    figure,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "lasso2d",
            "select2d",
        ],
    },
)

insight_html = (
    '<div class="insight-card">'
    '<div class="insight-title">📈 Key insight</div>'
    '<div class="insight-text">'
    'The example scores show gradual improvement over four weekly check-ins. '
    'Version 3 will eventually calculate insights from the user’s actual '
    'assessment history.'
    '</div>'
    '</div>'
)

st.markdown(insight_html, unsafe_allow_html=True)

st.write("")
st.markdown("## Planned features")

features = [
    "Weekly DASS-21 check-ins",
    "Personal assessment history",
    "Depression, anxiety, and stress trends",
    "Private mood journaling",
    "Exportable progress reports",
]

for feature in features:
    st.markdown(f"✅ &nbsp; {feature}")

render_footer()