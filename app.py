import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AstroGeo AI", page_icon="🪐", layout="wide")

# --- STAR THEME CSS (USE .stApp) ---
st.markdown("""
    <style>
    .stApp {
        background: 
            radial-gradient(ellipse at center, #000015 40%, #000028 100%),
            url("https://www.transparenttextures.com/patterns/green-dust-and-scratches.png");
        background-attachment: fixed;
        background-repeat: repeat;
        background-size: auto, cover;
    }
    .block-container {
        background: rgba(10, 10, 40, 0.86) !important;
        color: #eaf1fa !important;
        border-radius: 18px;
        padding: 2.2rem 2.6rem;
        margin-bottom: 28px;
        box-shadow: 0 8px 24px #13235099 !important;
    }
    .stButton>button {
        background: linear-gradient(92deg, #224ecf 40%, #04aacb 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.07em !important;
        font-weight: 600 !important;
        padding: 10px 32px !important;
        transition: 0.2s !important;
    }
    .stButton>button:hover {
        background: linear-gradient(92deg,#108be7 20%,#0975d5 100%) !important;
        color: #fff !important;
        box-shadow: 0 4px 24px #00cfff44 !important;
    }
    .query-area input {
        font-size: 18px !important;
        background: #131f33 !important;
        color: #fff !important;
        border: 1.5px solid #446cb3 !important;
        border-radius: 7px !important;
    }
    ::placeholder {
        color: #b6bbce !important;
        opacity: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<div class='block-container'>", unsafe_allow_html=True)
st.markdown("""
    <div style='font-size:48px; text-align:center; letter-spacing:2px; font-weight:bold;'>
        🪐 <span style='color:#70bbff;'>AstroGeo AI</span>
    </div>
    <div style='font-size:1.32em; text-align:center; color:#a0cfff; margin-top:-14px; margin-bottom:12px;'>
         ISRO Data Assistant<br>
        Explore weather, rainfall, climate, and disaster data — Powered by Bhuvan, VEDAS, MOSDAC
    </div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- QUERY INPUT SECTION ---
st.markdown("<div class='block-container'>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    user_query = st.text_input(
        label="Ask your question (e.g., 'rainfall in Kerala June 2023', 'recent flood alerts Assam')",
        placeholder="Enter your natural language query here...",
        key="astrogeo_query",
    )
    # --- POETIC PROMPT TAGLINE ---
st.markdown(
    "<div style='text-align:center; font-size:1.25em; color:#b0cfff; margin-top:-18px; margin-bottom:14px;'>"
    "✨ Wonder something? Space might know. ✨"
    "</div>",
    unsafe_allow_html=True
)

with col2:
    submit = st.button("🚀 Search", key="astrogeo_btn")
st.markdown("</div>", unsafe_allow_html=True)

# --- RESPONSE OUTPUT SECTION ---
st.markdown("<div class='block-container'>", unsafe_allow_html=True)
if submit and user_query:
    st.success(f"**You asked:** {user_query}")
    with st.spinner("🌌 Gathering data from ISRO portals..."):
        time.sleep(1.25)  # Simulate loading delay

        st.markdown(
            """
            <b style='color:#70bbff;'>Demo Output:</b> This area will display map, charts, or tables from Bhuvan, VEDAS, or MOSDAC data.<br>
            <span style='color:#c9e8ff;'>Connect your data retrieval and visualization code here.</span>
            """,
            unsafe_allow_html=True,
        )

        # --- DEMO CHART ---
        df = pd.DataFrame({
            "Month": ["April", "May", "June", "July", "August"],
            "Rainfall (mm)": [52, 120, 253, 410, 321]
        })
        fig = px.line(
            df, x="Month", y="Rainfall (mm)",
            markers=True, title="Rainfall Trend (Demo Data)",
            template="plotly_dark"
        )
        fig.update_traces(line_color="#1ccaff", marker_color="#fff")
        st.plotly_chart(fig, use_container_width=True)

        # --- DEMO MAP ---
        st.write("**Sample Map:** (Replace with your geospatial data)")
        fmap = folium.Map(location=[22, 78], zoom_start=5, tiles=None)
        folium.TileLayer("CartoDB dark_matter").add_to(fmap)
        folium.Marker([23.2, 77.5], popup="Sample Location").add_to(fmap)
        st_folium(fmap, width=700, height=360)

else:
    st.info("Type your question above and click 🚀 Search to fetch ISRO data.")

st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER SECTION ---
st.markdown(
    """
    <div style="text-align:center; margin-top:3rem; color:#70bbff; font-size:1.04em;">
        <b>AstroGeo AI</b> — One Universe of India's Space & Earth Data<br>
        Powered by&nbsp;
        <a href="https://bhuvan.nrsc.gov.in" target="_blank" style="color:#70bbff;">Bhuvan</a> |&nbsp;
        <a href="https://vedas.sac.gov.in" target="_blank" style="color:#70bbff;">VEDAS</a> |&nbsp;
        <a href="https://mosdac.gov.in" target="_blank" style="color:#70bbff;">MOSDAC</a>
    </div>
    """,
    unsafe_allow_html=True,
)
