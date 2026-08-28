import streamlit as st
from src.components import render_page_header, render_section_header

def render_page():
    """
    Renders the CPI Integration page.
    """
    render_page_header(
        title="CPI Integration Analysis",
        subtitle="Exploring how high-frequency airfare indices can support official Consumer Price Index (CPI) statistics."
    )
    
    st.info(
        "💡 **Statistical Role Disclaimer**: FareForce is an analytical data tool and prototype. "
        "It does NOT calculate the official Consumer Price Index (CPI) of India. Instead, it demonstrates "
        "how automated high-frequency indicators could act as an analytical source to support official statistics.",
        icon="💡"
    )
    
    st.markdown(
        "The Consumer Price Index (CPI) measures the average change over time in the prices of goods and services "
        "consumed by households. Air travel is included in the transport and communication subgroup. However, airfares "
        "are exceptionally volatile, making them a prime candidate for automated, high-frequency measurement."
    )
    
    # Flow diagram
    render_section_header("Conceptual Data Integration Flow")
    
    integration_flow_html = """
    <div style="background-color: #ffffff; padding: 25px; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 25px;">
        <div style="display: flex; flex-direction: column; align-items: center; max-width: 500px; margin: 0 auto;">
            <div style="background-color: #0f2d59; color: white; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 500; font-size: 0.9rem;">
                Daily Airfare Observations (Automated Scraping)
            </div>
            <div style="color: #64748b; font-size: 1.1rem; font-weight: bold; margin: 3px 0;">↓</div>
            <div style="background-color: #f1f5f9; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 500; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Strict Data Cleaning & Validation Filters
            </div>
            <div style="color: #64748b; font-size: 1.1rem; font-weight: bold; margin: 3px 0;">↓</div>
            <div style="background-color: #f1f5f9; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 500; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Route/Airline Aggregation (Jevons Formula)
            </div>
            <div style="color: #64748b; font-size: 1.1rem; font-weight: bold; margin: 3px 0;">↓</div>
            <div style="background-color: #f1f5f9; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 500; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                Calculated Daily Airfare Price Index
            </div>
            <div style="color: #64748b; font-size: 1.1rem; font-weight: bold; margin: 3px 0;">↓</div>
            <div style="background-color: #f1f5f9; color: #0f2d59; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 500; font-size: 0.9rem; border: 1px solid #cbd5e1;">
                High-Frequency Air Travel Price Signal
            </div>
            <div style="color: #64748b; font-size: 1.1rem; font-weight: bold; margin: 3px 0;">↓</div>
            <div style="background-color: #0d9488; color: white; padding: 10px; border-radius: 4px; text-align: center; width: 100%; font-weight: 500; font-size: 0.9rem;">
                Potential CPI Analytical Support (MOSPI DIID)
            </div>
        </div>
    </div>
    """
    st.markdown(integration_flow_html, unsafe_allow_html=True)
    
    # 4 core subsections explaining details
    render_section_header("CPI Augmentation Details")
    
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; gap: 20px;">
            <div style="background-color: white; padding: 20px; border: 1px solid #e2e8f0; border-radius: 6px;">
                <h5 style="color: #0f2d59; font-weight: 600; margin-top: 0;">1. Current CPI Data Collection Challenge</h5>
                <p style="font-size: 0.95rem; line-height: 1.6; color: #334155; margin-bottom: 0;">
                    Traditional CPI data collection relies on scheduled offline visits or manual online checks of static shops 
                    and services, usually on a monthly frequency. For industries like air travel, where ticket prices update 
                    multiple times a day based on booking windows and seat supply, single-day manual checks fail to capture 
                    the actual weighted average price paid by consumers.
                </p>
            </div>
            <div style="background-color: white; padding: 20px; border: 1px solid #e2e8f0; border-radius: 6px;">
                <h5 style="color: #0f2d59; font-weight: 600; margin-top: 0;">2. Why Airfare Requires High-Frequency Observation</h5>
                <p style="font-size: 0.95rem; line-height: 1.6; color: #334155; margin-bottom: 0;">
                    Airfares behave dynamically due to algorithmic yield management. Standard pricing shifts occur during 
                    festivals (Diwali, Holi), holiday seasons, and business cycles. Furthermore, the pricing structure 
                    differs dramatically based on advance booking windows. A robust CPI model should track pricing curves 
                    across all lead times (e.g., 1 day, 7 days, 30 days) to accurately represent inflation in the transport sector.
                </p>
            </div>
            <div style="background-color: white; padding: 20px; border: 1px solid #e2e8f0; border-radius: 6px;">
                <h5 style="color: #0f2d59; font-weight: 600; margin-top: 0;">3. How FareForce Provides Additional Airfare Information</h5>
                <p style="font-size: 0.95rem; line-height: 1.6; color: #334155; margin-bottom: 0;">
                    FareForce demonstrates how automated scraping workers can run daily to gather thousands of price quotes. 
                    This high-frequency feed provides:
                </p>
                <ul style="font-size: 0.95rem; line-height: 1.6; color: #334155; margin-top: 10px; margin-bottom: 0;">
                    <li><strong>Continuous Observation:</strong> Eliminates month-day sampling errors by tracking daily trends.</li>
                    <li><strong>Granular Attributes:</strong> Tracks individual carriers, routes, and booking windows separately.</li>
                    <li><strong>Statistical Verification:</strong> Uses clean Jevons calculations that are immediately comparable to CPI index formulas.</li>
                </ul>
            </div>
            <div style="background-color: white; padding: 20px; border: 1px solid #e2e8f0; border-radius: 6px;">
                <h5 style="color: #0f2d59; font-weight: 600; margin-top: 0;">4. Potential Benefits for Statistical Analysis</h5>
                <p style="font-size: 0.95rem; line-height: 1.6; color: #334155; margin-bottom: 0;">
                    Integrating high-frequency air travel price signals offers significant advantages:
                </p>
                <ul style="font-size: 0.95rem; line-height: 1.6; color: #334155; margin-top: 10px; margin-bottom: 0;">
                    <li><strong>Early Warning Signal:</strong> Acts as a leading indicator of travel-sector inflation before official CPI monthly releases.</li>
                    <li><strong>Cross-Validation Feed:</strong> Serves as a reference source to cross-check offline manual survey returns.</li>
                    <li><strong>Policy Formulation:</strong> Provides government planners and aviation regulators with high-resolution indicators to monitor market concentration and price dispersion.</li>
                </ul>
            </div>
        </div>
    """,
        unsafe_allow_html=True
    )
