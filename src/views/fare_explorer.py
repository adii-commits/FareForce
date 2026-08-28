import streamlit as st
import pandas as pd
from src.components import render_page_header, render_section_header, render_kpi_card, plot_fare_distribution
import plotly.express as px

def render_page(df_clean):
    """
    Renders the Fare Explorer page.
    """
    render_page_header(
        title="Fare Explorer",
        subtitle="Explore and filter domestic airfares based on route, carrier, and advance booking window."
    )
    
    # 1. Filter Section (Multi-column Layout)
    st.markdown("### Interactive Filters")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        origins = sorted(df_clean["origin"].unique())
        selected_origin = st.selectbox("Origin", options=["All"] + list(origins))
        
    with col_f2:
        # Filter destinations based on origin to avoid selecting impossible routes
        if selected_origin != "All":
            destinations = sorted(df_clean[df_clean["origin"] == selected_origin]["destination"].unique())
        else:
            destinations = sorted(df_clean["destination"].unique())
        selected_dest = st.selectbox("Destination", options=["All"] + list(destinations))
        
    with col_f3:
        airlines = sorted(df_clean["airline"].unique())
        selected_airline = st.selectbox("Airline", options=["All"] + list(airlines))
        
    with col_f4:
        windows = [1, 3, 7, 15, 30, 45]
        selected_window = st.selectbox(
            "Booking Window", 
            options=["All"] + [f"{w} Day{'s' if w > 1 else ''}" for w in windows]
        )
        
    # 2. Apply Filters
    df_filtered = df_clean.copy()
    
    if selected_origin != "All":
        df_filtered = df_filtered[df_filtered["origin"] == selected_origin]
        
    if selected_dest != "All":
        df_filtered = df_filtered[df_filtered["destination"] == selected_dest]
        
    if selected_airline != "All":
        df_filtered = df_filtered[df_filtered["airline"] == selected_airline]
        
    if selected_window != "All":
        window_val = int(selected_window.split(" ")[0])
        df_filtered = df_filtered[df_filtered["booking_window"] == window_val]
        
    # 3. Check for empty dataframe
    if df_filtered.empty:
        st.warning("⚠️ No quotes match the selected filters. Please adjust your selections.")
        return
        
    # 4. Calculate Summary Stats for Filtered Data
    avg_fare = df_filtered["fare"].mean()
    min_fare = df_filtered["fare"].min()
    max_fare = df_filtered["fare"].max()
    num_quotes = len(df_filtered)
    
    # Render Metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        render_kpi_card("Average Fare", f"₹{avg_fare:,.0f}", None, "", "Average fare for current filter selection")
    with col_m2:
        render_kpi_card("Minimum Fare", f"₹{min_fare:,.0f}", None, "", "Lowest recorded fare in this subset")
    with col_m3:
        render_kpi_card("Maximum Fare", f"₹{max_fare:,.0f}", None, "", "Highest recorded fare in this subset")
    with col_m4:
        render_kpi_card("Quotes Ingested", f"{num_quotes:,}", None, "", "Number of quotes matching filters")
        
    # 5. Summary Table by Airline
    render_section_header("Summary Table by Airline", "Carrier performance comparison for the selected filter combination")
    
    airline_grouped = df_filtered.groupby("airline").agg(
        avg_fare=("fare", "mean"),
        min_fare=("fare", "min"),
        max_fare=("fare", "max"),
        quotes_count=("fare", "count")
    ).reset_index()
    
    # Format summary table
    summary_table = airline_grouped.copy()
    summary_table.columns = ["Airline", "Average Fare (INR)", "Minimum Fare (INR)", "Maximum Fare (INR)", "Quotes Ingested"]
    summary_table["Average Fare (INR)"] = summary_table["Average Fare (INR)"].apply(lambda x: f"₹{x:,.2f}")
    summary_table["Minimum Fare (INR)"] = summary_table["Minimum Fare (INR)"].apply(lambda x: f"₹{x:,.2f}")
    summary_table["Maximum Fare (INR)"] = summary_table["Maximum Fare (INR)"].apply(lambda x: f"₹{x:,.2f}")
    summary_table["Quotes Ingested"] = summary_table["Quotes Ingested"].apply(lambda x: f"{x:,}")
    
    st.table(summary_table)
    
    # 6. Comparison Charts
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        # Airline Comparison Chart
        color_map = {
            "IndiGo": "#0d9488",
            "Air India": "#0f2d59",
            "SpiceJet": "#64748b",
            "Akasa Air": "#38bdf8"
        }
        fig_comp = px.bar(
            airline_grouped,
            x="airline",
            y="avg_fare",
            color="airline",
            color_discrete_map=color_map,
            labels={"avg_fare": "Average Fare (INR)", "airline": "Airline"},
            title="Average Fare Comparison by Airline"
        )
        fig_comp.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(linecolor='#cbd5e1', title=""),
            yaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1', title="Average Fare (INR)"),
            margin=dict(l=10, r=10, t=40, b=10),
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
    with col_c2:
        # Fare Distribution Histogram
        fig_dist = plot_fare_distribution(df_filtered, title="Fare Distribution for Selection")
        st.plotly_chart(fig_dist, use_container_width=True)
        
    # Data notice
    st.caption("ℹ️ Fares represent prototype/demonstration values. All price figures are in Indian Rupees (INR).")
