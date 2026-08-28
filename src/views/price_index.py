import streamlit as st
import pandas as pd
from src.components import render_page_header, render_section_header, render_kpi_card, plot_index_line_chart
from src.calculations import calculate_chained_jevons_index, get_route_level_indices

def render_page(df_clean):
    """
    Renders the Airfare Price Index page.
    """
    render_page_header(
        title="Airfare Price Index",
        subtitle="Historical trend analysis of the domestic airfare index using the Chained Jevons methodology."
    )
    
    st.markdown(
        "The airfare index measures changes in domestic passenger flight prices relative to a selected "
        "base period. This index aggregates fare data dynamically across multiple carriers, booking windows, and routes."
    )
    
    # 1. Base Calculations
    index_df = calculate_chained_jevons_index(df_clean)
    
    if index_df.empty:
        st.warning("No data available to calculate index.")
        return
        
    current_index = index_df.iloc[-1]["index_value"]
    base_index = 100.0
    total_change_pct = ((current_index - base_index) / base_index) * 100
    
    # Time window selector
    st.markdown("### Index Controls")
    time_window = st.radio(
        "Select Time Horizon:",
        options=["7 Days", "30 Days", "90 Days"],
        index=1, # Default 30 Days
        horizontal=True
    )
    
    # Filter index based on time window
    days_to_keep = 7 if time_window == "7 Days" else (30 if time_window == "30 Days" else 90)
    filtered_index_df = index_df.tail(days_to_keep)
    
    # Calculate stats for the selected window
    win_start_idx = filtered_index_df.iloc[0]["index_value"]
    win_end_idx = filtered_index_df.iloc[-1]["index_value"]
    win_change_pct = ((win_end_idx - win_start_idx) / win_start_idx) * 100
    
    # KPI Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Current Index Value", f"{win_end_idx:.2f}", None, "", "Current chained Jevons index value")
    with col2:
        render_kpi_card("Base Period Index", "100.00", None, "", "Base period index fixed value")
    with col3:
        render_kpi_card(
            "Period Change (%)", 
            f"{win_change_pct:+.2f}%", 
            win_change_pct, 
            f"{win_end_idx - win_start_idx:+.2f} index points",
            "Percentage change over the selected time horizon"
        )
        
    # Large index chart
    fig_index = plot_index_line_chart(
        filtered_index_df, 
        title=f"Chained Jevons Geometric Mean Index Trend - Last {days_to_keep} Days"
    )
    st.plotly_chart(fig_index, use_container_width=True)
    
    # Route level index table
    render_section_header("Route-Level Index Performance", "Indices calculated independently per route over the full 90-day period")
    
    # Calculate route-level indices
    route_indices = get_route_level_indices(df_clean)
    
    # Format Route table
    if not route_indices.empty:
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            # Custom formatting for Display
            display_df = route_indices.copy()
            display_df.columns = ["Route", "Current Index (Base=100)", "30-Day Change (%)"]
            
            # Format numbers to text with positive sign for changes
            display_df["30-Day Change (%)"] = display_df["30-Day Change (%)"].apply(lambda x: f"{x:+.2f}%" if x != 0 else "0.00%")
            display_df["Current Index (Base=100)"] = display_df["Current Index (Base=100)"].apply(lambda x: f"{x:.2f}")
            
            st.table(display_df)
            
        with col_t2:
            st.markdown(
                """
                <div style="background-color: #f1f5f9; padding: 15px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.9rem;">
                    <h5 style="color:#0f2d59; margin-top:0; font-weight:600;">How to Interpret the Index</h5>
                    <ul style="margin-bottom:0; padding-left: 20px;">
                        <li><strong>Base Index = 100</strong>: This is the starting point of the index measurement period.</li>
                        <li><strong>Index above 100</strong>: Fares are higher than the base period average (e.g., an index of 105.50 means prices are 5.5% higher).</li>
                        <li><strong>Index below 100</strong>: Fares are lower than the base period average (e.g., an index of 97.20 means prices are 2.8% lower).</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.caption("Note: Route indices reflect the price changes within specific routes, relative to their own start dates inside the prototype dataset.")
