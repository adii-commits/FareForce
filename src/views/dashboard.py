import streamlit as st
import datetime
from src.components import render_page_header, render_section_header, render_kpi_card, plot_index_line_chart, plot_grouped_bar_fares
from src.calculations import calculate_chained_jevons_index

def render_page(df_raw, df_clean):
    """
    Renders the Dashboard page.
    """
    render_page_header(
        title="FareForce",
        subtitle="High-frequency monitoring and statistical analysis of domestic airfare prices in India."
    )
    
    # Calculate required stats
    # 1. Total Quotes Ingested (raw observations)
    total_quotes = len(df_raw)
    
    # 2. Routes Covered
    num_routes = df_clean["route"].nunique()
    
    # 3. Latest Average Fare
    latest_date = df_clean["date"].max()
    latest_day_df = df_clean[df_clean["date"] == latest_date]
    latest_avg_fare = latest_day_df["fare"].mean()
    
    # 4. Calculate Index Series
    index_df = calculate_chained_jevons_index(df_clean)
    current_index = index_df.iloc[-1]["index_value"] if not index_df.empty else 100.0
    
    # Get 30 days change for delta
    if len(index_df) >= 30:
        base_30_idx = len(index_df) - 30
        index_30_days_ago = index_df.iloc[base_30_idx]["index_value"]
        delta_val = current_index - index_30_days_ago
        delta_pct = (delta_val / index_30_days_ago) * 100
        delta_text = f"{delta_val:+.2f} ({delta_pct:+.2f}%) vs 30d ago"
    else:
        delta_val = 0.0
        delta_text = "N/A"
        
    # Latest fare delta vs previous day
    prev_date = sorted(df_clean["date"].unique())[-2] if df_clean["date"].nunique() >= 2 else None
    if prev_date:
        prev_day_df = df_clean[df_clean["date"] == prev_date]
        prev_avg_fare = prev_day_df["fare"].mean()
        fare_delta = latest_avg_fare - prev_avg_fare
        fare_delta_pct = (fare_delta / prev_avg_fare) * 100
        fare_delta_text = f"₹{fare_delta:+.0f} ({fare_delta_pct:+.2f}%) vs yesterday"
    else:
        fare_delta = 0.0
        fare_delta_text = "N/A"

    # Banner / Disclaimer
    st.info(
        "ℹ️ **Prototype Data Environment Notice**: All data displayed below belongs to the **Prototype Dataset**. "
        "This platform is a statistical simulation for the Smart India Hackathon 2026. The data is generated "
        "and is not currently live scraped from airline portals.",
        icon=None
    )
    
    # KPI Grid
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card("Current Airfare Index", f"{current_index:.2f}", delta_val, delta_text, "Chained Jevons index relative to the base day")
    with col2:
        render_kpi_card("Base Index", "100.00", 0, "Fixed Base Period", "Base period index value fixed at 100")
    with col3:
        render_kpi_card("Latest Average Fare", f"₹{latest_avg_fare:,.0f}", fare_delta, fare_delta_text, "Average fare across all routes and carriers on the latest day")
    with col4:
        render_kpi_card("Total Quotes Ingested", f"{total_quotes:,}", None, "", "Total rows of data collected (including duplicate/invalid quotes before validation)")
    with col5:
        render_kpi_card("Routes Covered", f"{num_routes}", None, "", "Number of high-density domestic routes monitored")
        
    # Index Chart Section
    render_section_header("30-Day Airfare Price Index Trend", "Calculated daily using the Chained Jevons Geometric Mean methodology")
    
    # Get last 30 days of index
    index_30d = index_df.tail(30)
    fig_line = plot_index_line_chart(index_30d, title="Chained Jevons Geometric Mean Index (Last 30 Days)")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Bar Chart Section
    render_section_header("Average Fare by Route & Airline", "Price comparison across key domestic routes based on the prototype dataset")
    
    # Generate grouped bar chart
    fig_bar = plot_grouped_bar_fares(df_clean, title="Aggregated Average Fares (INR) by Route & Operating Airline")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Small footnotes
    st.markdown(
        "<div style='text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 20px;'>"
        "Data source status: Operational simulated environment | Method: Chained Jevons Index"
        "</div>",
        unsafe_allow_html=True
    )
