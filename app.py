import streamlit as st
import datetime

# 1. Page Config
st.set_page_config(
    page_title="FareForce - Real-Time Airfare Price Index for India",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Reusable Components & Calculations Imports
from src.components import inject_custom_styles
from src.data_generator import generate_prototype_dataset
from src.calculations import clean_data

# 3. Cache Data Generation and Cleaning
# Using st.cache_data to prevent regeneration on every view update or slider slide
@st.cache_data
def get_cached_dataset():
    # Anchored to 2026-08-29 as specified by user instructions
    anchor_date = datetime.date(2026, 8, 29)
    df_raw = generate_prototype_dataset(end_date=anchor_date, num_days=90)
    df_clean, metrics = clean_data(df_raw)
    return df_raw, df_clean, metrics

df_raw, df_clean, metrics = get_cached_dataset()

# 4. Sidebar Branding & Custom Navigation
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 15px 0 10px 0;">
        <h2 style="color: white; margin: 0; font-size: 1.6rem; font-weight: 700; letter-spacing: 1px; line-height:1.1;">FAREFORCE</h2>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin-top: 5px; margin-bottom: 0;">Real-Time Airfare Price Index</p>
    </div>
    <hr style="margin-top: 10px; margin-bottom: 20px; border-color: rgba(255,255,255,0.15);">
    """,
    unsafe_allow_html=True
)

# Render organized sections in the navigation sidebar
st.sidebar.markdown("<p style='font-size: 0.7rem; color: rgba(255,255,255,0.5); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;'>Overview</p>", unsafe_allow_html=True)
nav_overview = ["Dashboard"]

st.sidebar.markdown("<p style='font-size: 0.7rem; color: rgba(255,255,255,0.5); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 15px; margin-bottom: 4px;'>Analytics</p>", unsafe_allow_html=True)
nav_analytics = ["Airfare Price Index", "Fare Explorer", "Route Analysis", "Booking Window Analysis"]

st.sidebar.markdown("<p style='font-size: 0.7rem; color: rgba(255,255,255,0.5); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 15px; margin-bottom: 4px;'>Data</p>", unsafe_allow_html=True)
nav_data = ["Data Collection", "Data Quality"]

st.sidebar.markdown("<p style='font-size: 0.7rem; color: rgba(255,255,255,0.5); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 15px; margin-bottom: 4px;'>Methodology</p>", unsafe_allow_html=True)
nav_methodology = ["Index Methodology", "CPI Integration"]

# Master navigation list
all_pages = nav_overview + nav_analytics + nav_data + nav_methodology

page_selection = st.sidebar.radio(
    "Navigation Select",
    options=all_pages,
    label_visibility="collapsed"
)

# Sidebar Footer Section
st.sidebar.markdown("<br><br><hr style='border-color: rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div style="font-size: 0.72rem; color: rgba(255,255,255,0.6); line-height: 1.5; padding-bottom: 10px;">
        <strong>Smart India Hackathon 2026</strong><br>
        SIH26056 | Smart Automation<br><br>
        <strong>MOSPI | Prototype</strong><br>
        DIID Data Informatics
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Inject styles and route to selected views
inject_custom_styles()

if page_selection == "Dashboard":
    from src.views.dashboard import render_page
    render_page(df_raw, df_clean)
elif page_selection == "Airfare Price Index":
    from src.views.price_index import render_page
    render_page(df_clean)
elif page_selection == "Fare Explorer":
    from src.views.fare_explorer import render_page
    render_page(df_clean)
elif page_selection == "Route Analysis":
    from src.views.route_analysis import render_page
    render_page(df_clean)
elif page_selection == "Booking Window Analysis":
    from src.views.booking_window import render_page
    render_page(df_clean)
elif page_selection == "Data Collection":
    from src.views.data_collection import render_page
    render_page(df_raw, df_clean)
elif page_selection == "Data Quality":
    from src.views.data_quality import render_page
    render_page(df_raw)
elif page_selection == "Index Methodology":
    from src.views.methodology import render_page
    render_page()
elif page_selection == "CPI Integration":
    from src.views.cpi_integration import render_page
    render_page()
