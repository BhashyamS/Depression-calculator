import plotly.graph_objects as go
import streamlit as st

MAX_SCORE = 42

def render_radar_chart(results: dict):
    categories = ["Depression", "Anxiety", "Stress"]
    values = [results[c]["score"] / MAX_SCORE * 100 for c in categories]
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        line=dict(color="#789F8B", width=3),
        fillcolor="rgba(120,159,139,.28)",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0,100], ticksuffix="%")),
        showlegend=False,
        height=420,
        margin=dict(l=40,r=40,t=20,b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption("Percentages are for visual comparison only.")

def render_score_bars(results: dict):
    for scale in ["Depression", "Anxiety", "Stress"]:
        r = results[scale]
        width = min(r["score"] / MAX_SCORE * 100, 100)
        st.markdown(f"""
        <div class="score-bar-card">
            <div class="score-bar-header">
                <span>{scale}</span><span style="color:{r['color']}">{r['score']} · {r['severity']}</span>
            </div>
            <div class="score-bar-track">
                <div class="score-bar-fill" style="width:{width}%;background:{r['color']}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
