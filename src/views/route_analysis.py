import streamlit as st
import pandas as pd
import numpy as np
from src.components import render_page_header, render_section_header, render_kpi_card, plot_index_line_chart
from src.calculations import calculate_chained_jevons_index
import plotly.express as px
import plotly.graph_objects as go

def render_page(df_clean):
    """
    Renders the Route Analysis page.
    """
    render_page_header(
        title="Route Analysis",
        subtitle="In-depth analysis of specific flight sectors including historical fare and index trends."
    )
    
    # Route selector
    routes = sorted(df_clean["route"].unique())
    selected_route = st.selectbox("Select Route Sector:", options=routes)
    
    # Filter dataset for selected route
    df_route = df_clean[df_clean["route"] == selected_route].copy()
    
    if df_route.empty:
        st.warning("No data available for this route.")
        return
        
    # Calculate stats for the selected route
    avg_fare = df_route["fare"].mean()
    min_fare = df_route["fare"].min()
    max_fare = df_route["fare"].max()
    num_quotes = len(df_route)
    
    # Calculate index series for this route
    route_index_df = calculate_chained_jevons_index(df_route)
    
    if not route_index_df.empty:
        current_idx = route_index_df.iloc[-1]["index_value"]
        
        # Calculate 30-day index change
        if len(route_index_df) >= 30:
            idx_30d_ago = route_index_df.iloc[-30]["index_value"]
            change_30d = ((current_idx - idx_30d_ago) / idx_30d_ago) * 100
            change_points = current_idx - idx_30d_ago
            change_text = f"{change_points:+.2f} ({change_30d:+.2f}%)"
        else:
            change_30d = 0.0
            change_text = "N/A (Dataset < 30 days)"
    else:
        current_idx = 100.0
        change_30d = 0.0
        change_text = "N/A"
        
    # KPI metrics grid
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Average Fare", f"₹{avg_fare:,.0f}", None, "", "Average fare for this route sector")
    with col2:
        render_kpi_card("Current Airfare Index", f"{current_idx:.2f}", change_30d, change_text, "Current airfare index for this specific route (Base = 100)")
    with col3:
        render_kpi_card("Quotes Ingested", f"{num_quotes:,}", None, "", "Total number of observations for this route sector")
        
    col4, col5 = st.columns(2)
    with col4:
        render_kpi_card("Minimum Fare", f"₹{min_fare:,.0f}", None, "", "Lowest price observed on this route")
    with col5:
        render_kpi_card("Maximum Fare", f"₹{max_fare:,.0f}", None, "", "Highest price observed on this route")
        
    # Trends section
    render_section_header(f"Price & Index Trends for {selected_route}")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Daily Average Fare Trend
        daily_fares = df_route.groupby("date")["fare"].mean().reset_index()
        fig_fare_trend = go.Figure()
        fig_fare_trend.add_trace(go.Scatter(
            x=daily_fares["date"],
            y=daily_fares["fare"],
            mode="lines",
            line=dict(color="#0f2d59", width=2),
            name="Avg Fare"
        ))
        fig_fare_trend.update_layout(
            title=dict(text="Daily Average Fare Trend (INR)", font=dict(size=13, color="#0f2d59")),
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=35, b=10),
            height=250,
            xaxis=dict(linecolor="#cbd5e1", title=""),
            yaxis=dict(gridcolor="#e2e8f0", linecolor="#cbd5e1", title="Fare (INR)")
        )
        st.plotly_chart(fig_fare_trend, use_container_width=True)
        
    with col_g2:
        # Route Index Trend
        if not route_index_df.empty:
            fig_idx_trend = plot_index_line_chart(
                route_index_df, 
                title="Route-Specific Airfare Price Index (Base = 100)"
            )
            fig_idx_trend.update_layout(height=250, margin=dict(l=10, r=10, t=35, b=10))
            st.plotly_chart(fig_idx_trend, use_container_width=True)
            
    # Airline comparison for this route
    render_section_header("Airline Price Comparison", f"Average ticket pricing by operating airlines on the {selected_route} sector")
    
    airline_route = df_route.groupby("airline")["fare"].agg(["mean", "min", "max", "count"]).reset_index()
    
    col_chart, col_table = st.columns([1, 1])
    
    with col_chart:
        color_map = {
            "IndiGo": "#0d9488",
            "Air India": "#0f2d59",
            "SpiceJet": "#64748b",
            "Akasa Air": "#38bdf8"
        }
        fig_air_comp = px.bar(
            airline_route,
            x="airline",
            y="mean",
            color="airline",
            color_discrete_map=color_map,
            labels={"mean": "Average Fare (INR)", "airline": "Airline"},
            title="Average Fare by Airline on Route"
        )
        fig_air_comp.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=35, b=10),
            height=230,
            showlegend=False,
            xaxis=dict(linecolor="#cbd5e1", title=""),
            yaxis=dict(gridcolor="#e2e8f0", linecolor="#cbd5e1", title="")
        )
        st.plotly_chart(fig_air_comp, use_container_width=True)
        
    with col_table:
        # Format columns
        format_df = airline_route.copy()
        format_df.columns = ["Airline", "Avg Fare", "Min Fare", "Max Fare", "Quotes"]
        format_df["Avg Fare"] = format_df["Avg Fare"].apply(lambda x: f"₹{x:,.0f}")
        format_df["Min Fare"] = format_df["Min Fare"].apply(lambda x: f"₹{x:,.0f}")
        format_df["Max Fare"] = format_df["Max Fare"].apply(lambda x: f"₹{x:,.0f}")
        format_df["Quotes"] = format_df["Quotes"].apply(lambda x: f"{x:,}")
        st.table(format_df)
        
    # Route Summary Section
    render_section_header("Route Summary & Analytical Insights")
    
    # Build text dynamically from stats
    cheapest_airline = airline_route.loc[airline_route["mean"].idxmin()]["airline"]
    cheapest_avg = airline_route.loc[airline_route["mean"].idxmin()]["mean"]
    expensive_airline = airline_route.loc[airline_route["mean"].idxmax()]["airline"]
    expensive_avg = airline_route.loc[airline_route["mean"].idxmax()]["mean"]
    
    index_change_summary = ""
    if not route_index_df.empty:
        net_change = route_index_df.iloc[-1]["index_value"] - 100.0
        direction = "increased" if net_change > 0 else "decreased"
        index_change_summary = f"Over the full 90-day duration of this prototype dataset, the airfare index for this route has {direction} by {abs(net_change):.2f} index points, starting from base 100.00."
    
    st.markdown(
        f"""
        <div style="background-color: #ffffff; padding: 20px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
            <strong>Prototype Data Summary:</strong><br>
            For the <strong>{selected_route}</strong> sector, the average fare calculated across all observations is <strong>₹{avg_fare:,.2f}</strong>. 
            Within this dataset, the carrier with the lowest average fare is <strong>{cheapest_airline}</strong> (average ₹{cheapest_avg:,.2f}), 
            while the carrier with the highest average fare is <strong>{expensive_airline}</strong> (average ₹{expensive_avg:,.2f}).
            <br><br>
            {index_change_summary}
            The lowest price recorded was <strong>₹{min_fare:,.2f}</strong> and the highest was <strong>₹{max_fare:,.2f}</strong>.
            <br><br>
            <em style="color:#64748b;"><strong>Important Disclaimer:</strong> These observations are descriptive summaries of the generated <strong>Prototype Dataset</strong>. No external real-world conclusions, market-share generalizations, or economic claims should be made based on these simulated metrics.</em>
        </div>
        """,
        unsafe_allow_html=True
    )
