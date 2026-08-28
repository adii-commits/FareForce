import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def inject_custom_styles():
    """
    Injects custom CSS to style the Streamlit app to look like a professional
    government statistical dashboard.
    """
    st.markdown("""
        <style>
        /* Import Inter font or similar clean sans-serif */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #2d3748;
        }
        
        /* Main background */
        .stApp {
            background-color: #f8fafc;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #0f2d59 !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }
        
        /* Custom card style */
        .stat-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03);
            margin-bottom: 15px;
        }
        
        .stat-title {
            font-size: 0.75rem;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }
        
        .stat-value {
            font-size: 1.75rem;
            color: #0f2d59;
            font-weight: 700;
            line-height: 1.2;
        }
        
        .stat-delta {
            font-size: 0.85rem;
            margin-top: 4px;
            font-weight: 500;
        }
        
        .delta-up {
            color: #b91c1c; /* Soft red for index increase */
        }
        
        .delta-down {
            color: #047857; /* Soft green for index decrease */
        }
        
        .delta-neutral {
            color: #64748b;
        }
        
        /* Prototype badge */
        .proto-badge {
            background-color: #f1f5f9;
            color: #475569;
            border: 1px solid #cbd5e1;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        /* Styled table */
        .styled-table-container {
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            overflow: hidden;
            background: white;
            margin-bottom: 20px;
        }
        
        /* Sidebar styling custom overrides */
        [data-testid="stSidebar"] {
            background-color: #0f2d59 !important;
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.15) !important;
        }
        
        /* Radio button labels in sidebar */
        [data-testid="stSidebar"] label {
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        </style>
    """, unsafe_allow_html=True)

def render_page_header(title, subtitle=None, badge_text="Prototype Data Environment"):
    """
    Renders a standardized header for pages.
    """
    inject_custom_styles()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(title)
        if subtitle:
            st.markdown(f"<p style='font-size: 1.1rem; color: #475569; margin-top: -10px; margin-bottom: 20px;'>{subtitle}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: right; margin-top: 15px;'><span class='proto-badge'>{badge_text}</span></div>", unsafe_allow_html=True)
        
    st.markdown("<hr style='margin-top: 0; margin-bottom: 25px; border-color: #e2e8f0;'>", unsafe_allow_html=True)

def render_section_header(title, subtitle=None):
    """
    Renders a section header with a thin bottom border.
    """
    sub_html = f"<p style='font-size: 0.9rem; color: #64748b; margin-top: 2px; margin-bottom: 12px;'>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
        <div style="margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">
            <h3 style="color: #0f2d59; font-weight: 600; margin: 0; font-size: 1.25rem;">{title}</h3>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title, value, delta=None, delta_text="", help_text=None):
    """
    Renders a beautiful statistical KPI card.
    delta can be positive, negative, or zero.
    """
    delta_html = ""
    if delta is not None:
        if delta > 0:
            delta_html = f"<div class='stat-delta delta-up'>▲ {delta_text}</div>"
        elif delta < 0:
            delta_html = f"<div class='stat-delta delta-down'>▼ {delta_text}</div>"
        else:
            delta_html = f"<div class='stat-delta delta-neutral'>▬ {delta_text}</div>"
            
    tooltip = f" title='{help_text}'" if help_text else ""
    
    st.markdown(f"""
        <div class="stat-card"{tooltip}>
            <div class="stat-title">{title}</div>
            <div class="stat-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def plot_index_line_chart(df, date_col='date', val_col='index_value', title="Airfare Price Index Trend"):
    """
    Renders a professional line chart for index values.
    """
    fig = go.Figure()
    
    # Calculate range to ensure Base Index = 100 is always visible and chart is zoomed in
    min_val = df[val_col].min()
    max_val = df[val_col].max()
    
    # Add a dynamic y-axis padding to zoom in while guaranteeing 100 is visible
    padding = max(0.5, (max_val - min_val) * 0.15) if max_val != min_val else 1.0
    y_min = min(99.0, min_val - padding)
    y_max = max(101.0, max_val + padding)
    
    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df[val_col],
        mode='lines',
        line=dict(color='#0d9488', width=3), # Thicker Teal line
        name='Index Value',
        hovertemplate='Date: %{x}<br>Index: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color='#0f2d59', family='Inter')
        ),
        xaxis=dict(
            title=dict(text="Observation Date", font=dict(color='#64748b')),
            gridcolor='#f1f5f9',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            title=dict(text="Index Value (Base = 100)", font=dict(color='#64748b')),
            gridcolor='#e2e8f0',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b'),
            zeroline=False,
            range=[y_min, y_max] # Enforce clean zoomed range including 100
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=15, r=15, t=40, b=15),
        height=320,
        hovermode="x unified"
    )
    
    # Add base 100 horizontal reference line
    fig.add_shape(
        type="line",
        x0=df[date_col].min(),
        y0=100,
        x1=df[date_col].max(),
        y1=100,
        line=dict(color="#64748b", width=1.5, dash="dash") # Clearer dashed line
    )
    
    # Add annotation label for Base Index
    fig.add_annotation(
        x=df[date_col].min(),
        y=100,
        text="Base Index = 100",
        showarrow=False,
        yshift=10,
        xanchor="left",
        font=dict(size=10, color="#64748b", family='Inter')
    )
    
    return fig

def plot_grouped_bar_fares(df, route_col='route', fare_col='fare', airline_col='airline', title="Average Fare by Route & Airline"):
    """
    Renders a grouped bar chart using Plotly.
    """
    # Pre-aggregate data to avoid plotly warning
    df_grouped = df.groupby([route_col, airline_col])[fare_col].mean().reset_index()
    
    # Define a clean professional color palette (navy, teal, slate blue, greyish-blue)
    color_map = {
        "IndiGo": "#0d9488",    # Teal
        "Air India": "#0f2d59",  # Navy
        "SpiceJet": "#64748b",   # Steel Grey
        "Akasa Air": "#38bdf8"   # Sky Blue
    }
    
    fig = px.bar(
        df_grouped,
        x=route_col,
        y=fare_col,
        color=airline_col,
        barmode='group',
        color_discrete_map=color_map,
        labels={fare_col: "Average Fare (INR)", route_col: "Route", airline_col: "Airline"}
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color='#0f2d59', family='Inter')
        ),
        xaxis=dict(
            title=dict(font=dict(color='#64748b')),
            gridcolor='#f1f5f9',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            title=dict(text="Average Fare (INR)", font=dict(color='#64748b')),
            gridcolor='#e2e8f0',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=15, r=15, t=40, b=15),
        height=320,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(text="")
        )
    )
    
    return fig

def plot_booking_window_effect(df, window_col='booking_window', fare_col='fare', airline_col='airline', title="Average Fare vs. Booking Window"):
    """
    Renders a line plot displaying booking window on x-axis and average fare on y-axis, grouped by airline.
    """
    df_grouped = df.groupby([window_col, airline_col])[fare_col].mean().reset_index()
    
    # Custom sort for booking window (from 45 days advance down to 1 day advance)
    # We want x-axis to be numerical, but we can order it or just let numerical ordering handle it.
    # Note: booking windows are [1, 3, 7, 15, 30, 45].
    
    color_map = {
        "IndiGo": "#0d9488",
        "Air India": "#0f2d59",
        "SpiceJet": "#64748b",
        "Akasa Air": "#38bdf8"
    }
    
    fig = px.line(
        df_grouped,
        x=window_col,
        y=fare_col,
        color=airline_col,
        color_discrete_map=color_map,
        markers=True,
        labels={fare_col: "Average Fare (INR)", window_col: "Booking Window (Days Advance)"}
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color='#0f2d59', family='Inter')
        ),
        xaxis=dict(
            title=dict(text="Days Booked in Advance", font=dict(color='#64748b')),
            tickmode='array',
            tickvals=[1, 3, 7, 15, 30, 45],
            gridcolor='#f1f5f9',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            title=dict(text="Average Fare (INR)", font=dict(color='#64748b')),
            gridcolor='#e2e8f0',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=15, r=15, t=40, b=15),
        height=320,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(text="")
        )
    )
    
    return fig

def plot_fare_distribution(df, fare_col='fare', title="Fare Distribution (INR)"):
    """
    Renders a histogram of fares.
    """
    fig = px.histogram(
        df,
        x=fare_col,
        nbins=40,
        color_discrete_sequence=['#0f2d59'], # Navy
        opacity=0.85,
        labels={fare_col: "Fare (INR)"}
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color='#0f2d59', family='Inter')
        ),
        xaxis=dict(
            title=dict(text="Fare (INR)", font=dict(color='#64748b')),
            gridcolor='#f1f5f9',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            title=dict(text="Frequency Count", font=dict(color='#64748b')),
            gridcolor='#e2e8f0',
            linecolor='#cbd5e1',
            tickfont=dict(color='#64748b')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=15, r=15, t=40, b=15),
        height=280
    )
    
    return fig
