import streamlit as st
import pandas as pd
from src.components import (
    render_page_header,
    render_section_header,
    render_kpi_card,
    plot_index_line_chart,
    plot_grouped_bar_fares,
)
from src.calculations import calculate_chained_jevons_index, get_route_level_indices

AIRLINE_OPTIONS = ["IndiGo", "Air India", "SpiceJet", "Akasa Air"]
BOOKING_WINDOW_LABELS = {
    "3 Days in Advance": 3,
    "15 Days in Advance": 15,
    "30 Days in Advance": 30,
}


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

    st.markdown(
        """
        <style>
        /* Removable airline chips on this page */
        [data-testid="stMain"] span[data-baseweb="tag"] {
            background-color: #0f2d59 !important;
            color: #ffffff !important;
            border-radius: 999px !important;
            border: none !important;
        }
        [data-testid="stMain"] span[data-baseweb="tag"] svg {
            fill: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    render_section_header("Filters", "Charts and the chained index use only the selected airlines and booking window")

    col_air, col_win = st.columns([2, 1])
    with col_air:
        selected_airlines = st.multiselect(
            "Select Airlines",
            options=AIRLINE_OPTIONS,
            default=AIRLINE_OPTIONS,
            help="Add or remove carriers. Selected airlines appear as removable tags.",
        )
    with col_win:
        selected_window_label = st.selectbox(
            "Booking Window",
            options=list(BOOKING_WINDOW_LABELS.keys()),
            index=1,
            help="Restrict fares and the index to quotes booked this many days in advance.",
        )
    window_val = BOOKING_WINDOW_LABELS[selected_window_label]

    if not selected_airlines:
        st.warning("Select at least one airline to calculate the index and display fare charts.")
        return

    df_filtered = df_clean[
        df_clean["airline"].isin(selected_airlines)
        & (df_clean["booking_window"] == window_val)
    ].copy()

    if df_filtered.empty:
        st.warning("No prototype quotes match the selected airlines and booking window. Adjust the filters.")
        return

    index_df = calculate_chained_jevons_index(df_filtered)

    if index_df.empty:
        st.warning("No data available to calculate index.")
        return

    st.markdown("### Index Controls")
    time_window = st.radio(
        "Select Time Horizon:",
        options=["7 Days", "30 Days", "90 Days"],
        index=1,
        horizontal=True,
    )

    days_to_keep = 7 if time_window == "7 Days" else (30 if time_window == "30 Days" else 90)
    filtered_index_df = index_df.tail(days_to_keep)

    win_start_idx = filtered_index_df.iloc[0]["index_value"]
    win_end_idx = filtered_index_df.iloc[-1]["index_value"]
    win_change_pct = ((win_end_idx - win_start_idx) / win_start_idx) * 100

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

    airline_caption = ", ".join(selected_airlines)
    render_section_header(
        "Chained Jevons Geometric Mean Index",
        f"Daily chained index for {selected_window_label.lower()} · {airline_caption} · last {days_to_keep} observation days"
    )

    plot_df = filtered_index_df.copy()
    plot_df["date"] = pd.to_datetime(plot_df["date"])

    fig_index = plot_index_line_chart(
        plot_df,
        title="Chained Jevons Geometric Mean Index",
        xaxis_title="Date",
        yaxis_title="Price Index (Base = 100)",
        height=440,
        show_daily_markers=False,
        center_on_base=True,
        series_name="Daily Index",
    )
    st.plotly_chart(
        fig_index,
        width="stretch",
        config={
            "responsive": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
    )

    st.markdown(
        """
        <div style="display:flex; flex-wrap:wrap; gap:12px; margin: 8px 0 28px 0;">
            <div style="flex:1 1 200px; min-width:180px; background:#ffffff; border:1px solid #e2e8f0; border-radius:6px; padding:14px 16px;">
                <div style="font-size:0.72rem; font-weight:700; letter-spacing:0.04em; text-transform:uppercase; color:#64748b; margin-bottom:6px;">Base Index = 100</div>
                <div style="font-size:0.9rem; color:#334155; line-height:1.5;">The base period of the full series is fixed at <strong>100</strong>. Daily values on this chart are chained from that base (the dashed line).</div>
            </div>
            <div style="flex:1 1 200px; min-width:180px; background:#ffffff; border:1px solid #e2e8f0; border-radius:6px; padding:14px 16px;">
                <div style="font-size:0.72rem; font-weight:700; letter-spacing:0.04em; text-transform:uppercase; color:#64748b; margin-bottom:6px;">Above 100</div>
                <div style="font-size:0.9rem; color:#334155; line-height:1.5;">Fares are <strong>higher</strong> than the base period. An index of 105.50 means prices are 5.5% above base.</div>
            </div>
            <div style="flex:1 1 200px; min-width:180px; background:#ffffff; border:1px solid #e2e8f0; border-radius:6px; padding:14px 16px;">
                <div style="font-size:0.72rem; font-weight:700; letter-spacing:0.04em; text-transform:uppercase; color:#64748b; margin-bottom:6px;">Below 100</div>
                <div style="font-size:0.9rem; color:#334155; line-height:1.5;">Fares are <strong>lower</strong> than the base period. An index of 97.20 means prices are 2.8% below base.</div>
            </div>
            <div style="flex:1 1 200px; min-width:180px; background:#ffffff; border:1px solid #e2e8f0; border-radius:6px; padding:14px 16px;">
                <div style="font-size:0.72rem; font-weight:700; letter-spacing:0.04em; text-transform:uppercase; color:#64748b; margin-bottom:6px;">How it is calculated</div>
                <div style="font-size:0.9rem; color:#334155; line-height:1.5;">A <strong>chained Jevons geometric mean</strong> of matched price relatives for (route, airline, booking window), updated daily.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_section_header(
        "Average Fare by Route & Airline",
        f"Mean fares for {selected_window_label.lower()} among the selected carriers"
    )
    fig_bar = plot_grouped_bar_fares(
        df_filtered,
        title=f"Average Fare by Route & Airline — {selected_window_label}",
    )
    st.plotly_chart(
        fig_bar,
        width="stretch",
        config={
            "responsive": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
    )

    render_section_header(
        "Summary Table by Airline",
        f"Carrier statistics for {selected_window_label.lower()} using the selected airlines only"
    )
    airline_order = [a for a in AIRLINE_OPTIONS if a in selected_airlines]
    airline_grouped = (
        df_filtered.groupby("airline")
        .agg(
            avg_fare=("fare", "mean"),
            min_fare=("fare", "min"),
            max_fare=("fare", "max"),
            quotes_count=("fare", "count"),
        )
        .reindex(airline_order)
        .dropna(how="all")
        .reset_index()
    )
    summary_table = airline_grouped.copy()
    summary_table.columns = [
        "Airline",
        "Average Fare (INR)",
        "Minimum Fare (INR)",
        "Maximum Fare (INR)",
        "Quotes Ingested",
    ]
    summary_table["Average Fare (INR)"] = summary_table["Average Fare (INR)"].apply(lambda x: f"₹{x:,.2f}")
    summary_table["Minimum Fare (INR)"] = summary_table["Minimum Fare (INR)"].apply(lambda x: f"₹{x:,.2f}")
    summary_table["Maximum Fare (INR)"] = summary_table["Maximum Fare (INR)"].apply(lambda x: f"₹{x:,.2f}")
    summary_table["Quotes Ingested"] = summary_table["Quotes Ingested"].apply(lambda x: f"{int(x):,}")
    st.table(summary_table)

    render_section_header(
        "Route-Level Index Performance",
        "Indices calculated independently per route using the same airline and booking-window filters"
    )

    route_indices = get_route_level_indices(df_filtered)

    if not route_indices.empty:
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            display_df = route_indices.copy()
            display_df.columns = ["Route", "Current Index (Base=100)", "30-Day Change (%)"]
            display_df["30-Day Change (%)"] = display_df["30-Day Change (%)"].apply(
                lambda x: f"{x:+.2f}%" if x != 0 else "0.00%"
            )
            display_df["Current Index (Base=100)"] = display_df["Current Index (Base=100)"].apply(
                lambda x: f"{x:.2f}"
            )
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
                        <li><strong>Chained Jevons</strong>: Each day’s index is the previous day’s index multiplied by the geometric mean of matched price relatives.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.caption(
        "Note: Route indices reflect price changes within specific routes, relative to their own start dates "
        "inside the filtered prototype dataset. Removing an airline or changing the booking window recalculates "
        "the chained index and fare summaries from the same source data."
    )
