import streamlit as st

ICONS = {"Depression":"🌤️","Anxiety":"🫧","Stress":"🌿","General wellbeing":"💚"}

def render_recommendation_card(item: dict):
    st.markdown(f"""
    <div class="recommendation-card">
        <div class="recommendation-header">
            <div class="recommendation-icon">{ICONS.get(item['category'],'💚')}</div>
            <div>
                <div class="recommendation-category">{item['category']}</div>
                <div class="recommendation-title">{item['title']}</div>
            </div>
        </div>
        <div class="recommendation-description">{item['description']}</div>
    </div>
    """, unsafe_allow_html=True)
