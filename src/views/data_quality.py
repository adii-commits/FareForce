import streamlit as st
import pandas as pd
from src.components import render_page_header, render_section_header, render_kpi_card
from src.calculations import clean_data

def render_page(df_raw):
    """
    Renders the Data Quality page.
    """
    render_page_header(
        title="Data Quality & Integrity Dashboard",
        subtitle="Real-time statistical evaluation and preprocessing audits of the airfare price inputs."
    )
    
    # Calculate real statistics using our clean_data engine
    df_clean, metrics = clean_data(df_raw)
    
    st.markdown(
        "To ensure the airfare price index is statistically robust and fit for CPI analytical augmentation, "
        "raw collected prices must undergo standard data cleaning procedures. This page audits the quality "
        "characteristics of the ingested dataset."
    )
    
    # Render Dynamic Metrics Cards
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        render_kpi_card("Total Observations", f"{metrics['total_records']:,}", None, "", "Total raw records collected from sources")
    with col_q2:
        render_kpi_card("Valid Observations", f"{metrics['valid_records']:,}", None, "", "Cleaned observations ready for index calculation")
    with col_q3:
        # Completeness card
        completeness = metrics['completeness_pct']
        delta_label = "Healthy Threshold" if completeness >= 90 else "Review Threshold"
        render_kpi_card("Data Completeness", f"{completeness}%", 1 if completeness >= 90 else -1, delta_label, "Percentage of raw records that passed validation filters")
        
    col_q4, col_q5, col_q6 = st.columns(3)
    with col_q4:
        render_kpi_card("Duplicate Records", f"{metrics['duplicate_count']:,}", -1 if metrics['duplicate_count'] > 0 else 0, "Identified & Purged", "Identical rows removed")
    with col_q5:
        total_missing = metrics['missing_fare'] + metrics['missing_airline']
        render_kpi_card("Missing Values", f"{total_missing:,}", -1 if total_missing > 0 else 0, f"Fare: {metrics['missing_fare']} | Airline: {metrics['missing_airline']}", "Rows with null fares or carriers")
    with col_q6:
        render_kpi_card("Outliers Detected", f"{metrics['outliers_count']:,}", -1 if metrics['outliers_count'] > 0 else 0, "Flagged & Filtered", "Extreme values outside statistical limits")
        
    # Table of Raw Data Preview (Sample of first 5 rows with problems)
    render_section_header("Data Cleaning Audit Log")
    
    # Descriptions of each check
    st.markdown(
        """
        <div style="background-color: #ffffff; padding: 25px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin-bottom: 25px;">
            <h4 style="color:#0f2d59; font-weight:600; margin-top:0; border-bottom:1px solid #cbd5e1; padding-bottom:6px;">Data Processing Standards</h4>
            <div style="margin-top: 15px;">
                <strong>1. Data Validation:</strong><br>
                Every incoming observation is verified for correct data types (dates are parsed, fares must be positive floating numbers) and route verification against official Indian airports list (e.g. Origin and Destination codes are verified).
            </div>
            <div style="margin-top: 15px;">
                <strong>2. Missing Data Handling:</strong><br>
                Records containing missing prices (NaN) or missing airline labels are omitted from index calculation. For advanced studies, price imputation or carrier-matching estimation can be modeled.
            </div>
            <div style="margin-top: 15px;">
                <strong>3. Duplicate Detection:</strong><br>
                Duplicate records (exact matches across date, route, airline, travel date, booking window, and price) represent crawling or API collection errors. These are identified via row-hash matching and automatically purged to avoid artificial index weighting.
            </div>
            <div style="margin-top: 15px;">
                <strong>4. Outlier Detection (Grouped 1.5x IQR):</strong><br>
                Prices are grouped by <code>(route, booking_window)</code>. Within each group, we compute:
                <br>
                <code style="background-color: #f1f5f9; padding: 2px 5px; border-radius: 3px;">IQR = Q3 - Q1</code>, setting validation limits at 
                <code style="background-color: #f1f5f9; padding: 2px 5px; border-radius: 3px;">[Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]</code>. 
                Values outside this range are flagged as outliers (e.g. data input errors, mistake fares, or extreme single-seat business classes) and excluded to protect index stability.
            </div>
            <div style="margin-top: 15px;">
                <strong>5. Data Completeness:</strong><br>
                Data Completeness represents the proportion of ingested quotes that are fully valid, non-duplicate, and fall within acceptable price ranges. A completeness level above 95% indicates high scraping accuracy and stable input feeds.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display small sample of actual records before cleaning
    st.subheader("Ingested Data Audit Samples")
    st.markdown("A brief audit look at the first 5 records of the raw simulation dataset:")
    st.dataframe(df_raw.head(5), use_container_width=True)
