import streamlit as st
import pandas as pd
from src.components import render_page_header, render_section_header, plot_booking_window_effect

def render_page(df_clean):
    """
    Renders the Booking Window Analysis page.
    """
    render_page_header(
        title="Booking Window Analysis",
        subtitle="Analyzing the impact of advance booking duration on domestic airfares in India."
    )
    
    st.markdown(
        "Airline ticket prices vary heavily depending on the booking window (i.e., how many days in advance a seat "
        "is booked). This analysis explores this behavior across different carriers and routes."
    )
    
    # Airline filter
    st.markdown("### Controls")
    airlines = sorted(df_clean["airline"].unique())
    selected_airline = st.selectbox("Select Airline to Filter:", options=["All Airlines"] + list(airlines))
    
    # Filter dataset
    df_filtered = df_clean.copy()
    if selected_airline != "All Airlines":
        df_filtered = df_filtered[df_filtered["airline"] == selected_airline]
        
    # Group by booking window
    grouped = df_filtered.groupby("booking_window")["fare"].agg(["mean", "count"]).reset_index()
    grouped = grouped.sort_values(by="booking_window")
    
    # Visual Chart
    fig_window = plot_booking_window_effect(
        df_filtered, 
        title=f"Average Fare vs. Booking Window ({selected_airline})"
    )
    st.plotly_chart(fig_window, use_container_width=True)
    
    # Summary Table
    render_section_header("Booking Window Statistics Table", "Aggregated fares and observations per advance booking window")
    
    col_t1, col_t2 = st.columns([1.5, 1])
    
    with col_t1:
        # Format columns for output
        table_df = grouped.copy()
        table_df.columns = ["Booking Window", "Average Fare (INR)", "Number of Quotes"]
        table_df["Booking Window"] = table_df["Booking Window"].apply(lambda x: f"{x} Day{'s' if x > 1 else ''} Advance")
        table_df["Average Fare (INR)"] = table_df["Average Fare (INR)"].apply(lambda x: f"₹{x:,.2f}")
        table_df["Number of Quotes"] = table_df["Number of Quotes"].apply(lambda x: f"{x:,}")
        
        st.table(table_df)
        
    with col_t2:
        st.markdown(
            """
            <div style="background-color: #ffffff; padding: 20px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
                <h5 style="color:#0f2d59; margin-top:0; font-weight:600;">Pricing Dynamics & Market Factors</h5>
                <p>
                    Airfare pricing models are highly complex and governed by real-time inventory management. 
                    Factors influencing these price points include:
                </p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li><strong>Advance Booking Lead Times:</strong> Flights booked within 1-3 days of departure usually command a steep price premium because of urgent business demand.</li>
                    <li><strong>Route Demand & Capacity:</strong> High load factors (full flights) drive fares up, while lower-than-expected bookings can trigger discounts.</li>
                    <li><strong>Yield Management:</strong> Algorithms dynamically adjust prices to maximize total revenue per flight rather than selling every seat at a fixed price.</li>
                </ul>
                <p style="margin-top: 15px; font-weight: bold; color: #b91c1c;">
                    ⚠️ Important Pricing Note:
                </p>
                <p style="font-style: italic; color: #475569;">
                    While booking earlier (e.g., 30-45 days) generally correlates with lower average fares, 
                    this does not guarantee a lower price under all market conditions due to sudden promotional campaigns, 
                    demand shocks, or carrier pricing strategies.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
