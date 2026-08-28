import streamlit as st
import pandas as pd
import datetime
from src.components import render_page_header, render_section_header, render_kpi_card

def render_page(df_raw, df_clean):
    """
    Renders the Data Collection page.
    """
    render_page_header(
        title="Data Collection Architecture",
        subtitle="Operational architecture of automated airfare scraping and data pipeline pipelines."
    )
    
    st.info(
        "📝 **System Status Notice**: This application currently operates on a **Prototype Dataset**. "
        "The data sources listed below represent planned targets for the operational scraping architecture "
        "and are not currently actively scraped in this demonstration environment.",
        icon="📝"
    )
    
    # Ingestion Pipeline Diagram
    render_section_header("Conceptual Data Processing Pipeline")
    
    pipeline_html = """
    <div style="background-color: #ffffff; padding: 25px; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 25px;">
        <div style="display: flex; flex-direction: column; align-items: center; max-width: 500px; margin: 0 auto;">
            <!-- Step 1 -->
            <div style="background-color: #0f2d59; color: white; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #0f2d59;">
                Airline Portals & Online Travel Aggregators (OTAs)
            </div>
            <div style="color: #64748b; font-size: 1.25rem; font-weight: bold; margin: 5px 0;">↓</div>
            <!-- Step 2 -->
            <div style="background-color: #ffffff; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Data Collection (Automated Web Scraping Workers)
            </div>
            <div style="color: #64748b; font-size: 1.25rem; font-weight: bold; margin: 5px 0;">↓</div>
            <!-- Step 3 -->
            <div style="background-color: #ffffff; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Data Validation (Formatting & Range Checks)
            </div>
            <div style="color: #64748b; font-size: 1.25rem; font-weight: bold; margin: 5px 0;">↓</div>
            <!-- Step 4 -->
            <div style="background-color: #ffffff; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Normalization & Schema Mapping
            </div>
            <div style="color: #64748b; font-size: 1.25rem; font-weight: bold; margin: 5px 0;">↓</div>
            <!-- Step 5 -->
            <div style="background-color: #ffffff; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Duplicate Removal & Outlier Filtering
            </div>
            <div style="color: #64748b; font-size: 1.25rem; font-weight: bold; margin: 5px 0;">↓</div>
            <!-- Step 6 -->
            <div style="background-color: #ffffff; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Statistical Aggregation (Link Relative Computation)
            </div>
            <div style="color: #64748b; font-size: 1.25rem; font-weight: bold; margin: 5px 0;">↓</div>
            <!-- Step 7 -->
            <div style="background-color: #ffffff; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Chained Jevons Index Calculation
            </div>
            <div style="color: #64748b; font-size: 1.25rem; font-weight: bold; margin: 5px 0;">↓</div>
            <!-- Step 8 -->
            <div style="background-color: #0d9488; color: white; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 600; font-size: 0.9rem; border: 1px solid #0d9488;">
                Visual Analytics & CPI Integration Reports
            </div>
        </div>
    </div>
    """
    st.markdown(pipeline_html, unsafe_allow_html=True)
    
    # Planned Data Sources
    render_section_header("Planned / Target Data Sources")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(
            """
            <div style="background-color: white; padding: 15px; border-radius: 6px; border: 1px solid #e2e8f0; height: 100%;">
                <h5 style="color: #0f2d59; font-weight: 600; margin-top: 0;">Airline Direct Portals</h5>
                <p style="font-size: 0.9rem; color: #64748b;">Direct API or DOM queries to carrier reservation backends:</p>
                <ul style="font-size: 0.9rem; line-height: 1.6;">
                    <li><strong>IndiGo Portal</strong> (Primary low-cost carrier)</li>
                    <li><strong>Air India Portal</strong> (Full-service flag carrier)</li>
                    <li><strong>SpiceJet Portal</strong> (Low-cost budget carrier)</li>
                    <li><strong>Akasa Air Portal</strong> (New budget entrant)</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_s2:
        st.markdown(
            """
            <div style="background-color: white; padding: 15px; border-radius: 6px; border: 1px solid #e2e8f0; height: 100%;">
                <h5 style="color: #0f2d59; font-weight: 600; margin-top: 0;">Online Travel Aggregators (OTAs)</h5>
                <p style="font-size: 0.9rem; color: #64748b;">Aggregation platforms for multi-airline fare collection validation:</p>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; line-height: 1.6;">
                    <ul style="margin: 0; padding-left: 20px;">
                        <li><strong>MakeMyTrip</strong></li>
                        <li><strong>Yatra</strong></li>
                        <li><strong>EaseMyTrip</strong></li>
                    </ul>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li><strong>Cleartrip</strong></li>
                        <li><strong>Ixigo</strong></li>
                        <li><strong>Goibibo</strong></li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Prototype Dataset Metadata
    render_section_header("Prototype Data Ingestion Statistics", "Overview of the current active simulation database")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        render_kpi_card("Total Quotes Ingested", f"{len(df_raw):,}", None, "", "Raw observations loaded in the session")
    with col_m2:
        render_kpi_card("Monitored Routes", f"{df_clean['route'].nunique()}", None, "", "Unique airline route paths")
    with col_m3:
        render_kpi_card("Monitored Carriers", f"{df_clean['airline'].nunique()}", None, "", "Distinct scheduled domestic airlines")
    with col_m4:
        # Static refresh timestamp matching the anchor date
        render_kpi_card("Last Dataset Refresh", "2026-08-29 01:00", None, "", "Timestamp of the last scheduled backend file reload")
        
    st.caption("Notice: Active scraping scheduler is disabled in this prototype. Fares are supplied via local Python data model containers.")
