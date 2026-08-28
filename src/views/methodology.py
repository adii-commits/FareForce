import streamlit as st
from src.components import render_page_header, render_section_header

def render_page():
    """
    Renders the Index Methodology page.
    """
    render_page_header(
        title="Index Methodology",
        subtitle="Detailed explanation of the Chained Jevons Geometric Mean Index calculations."
    )
    
    # Official prototype disclaimer
    st.warning(
        "⚠️ **Methodology Status**: This methodology represents a **prototype methodology for high-frequency "
        "airfare price measurement**. It is designed for demonstration and statistical feasibility analysis. "
        "It does NOT calculate or represent the official Consumer Price Index (CPI) of India published by MOSPI."
    )
    
    # Text intro
    st.markdown(
        "Measuring changes in airfare is statistically challenging due to dynamic pricing models, seasonal flights, "
        "and shifting flight availability. The FareForce prototype uses a **Chained Jevons Geometric Mean Index** "
        "methodology, which is standard in modern price statistics."
    )
    
    # 6 Steps Section
    render_section_header("The 6-Step Ingestion & Index Pipeline")
    
    methodology_markdown = """
    1. **Data Collection**
       Gather price quotes from multiple channels. To ensure fair comparison, quotes are categorized into specific "matched products" based on: `(Route, Airline, Booking Window)`.
    
    2. **Data Cleaning**
       Purge duplicate records and missing data. Apply the 1.5x IQR method to isolate price outliers in each group, preventing data errors from skewing the final metrics.
       
    3. **Price Relatives Calculation**
       Compare the price of a matched item category today against its price yesterday. The price relative measures the percentage change.
       
    4. **Jevons Index (Geometric Mean)**
       Compute the geometric mean of all active price relatives on that day. The Jevons index is self-weighting and handles substitution effects (e.g., travellers choosing budget carriers when full-service fares spike).
       
    5. **Chaining**
       Multiply the daily change rate by the previous day's index. This aggregates daily price relatives into a continuous historical time-series index.
       
    6. **Aggregation**
       Compile route indices into national-level indicators using appropriate weights (e.g., flight passenger volumes).
    """
    st.markdown(methodology_markdown)
    
    # Mathematical explanation
    render_section_header("Mathematical Formulation")
    
    st.markdown("Here is the mathematical representation of the calculation:")
    
    st.markdown("#### 1. Price Relative")
    st.markdown("The price relative \( R_{c, t} \) for a matched product category \( c \) on day \( t \) relative to day \( t-1 \) is calculated as:")
    st.latex(r"R_{c, t} = \frac{P_{c, t}}{P_{c, t-1}}")
    st.markdown("Where \( P_{c, t} \) is the average price of category \( c \) on day \( t \), and \( P_{c, t-1} \) is its price on day \( t-1 \).")
    
    st.markdown("#### 2. Daily Jevons Link Relative")
    st.markdown("The link relative \( G_t \), representing the overall rate of price change on day \( t \), is the geometric mean of the price relatives for all matched categories \( M_t \) available on both days:")
    st.latex(r"G_t = \left( \prod_{c \in M_t} R_{c, t} \right)^{\frac{1}{|M_t|}} = \exp\left( \frac{1}{|M_t|} \sum_{c \in M_t} \ln(R_{c, t}) \right)")
    
    st.markdown("#### 3. Index Chaining")
    st.markdown("The index value for day \( t \), denoted \( I_t \), is calculated by chaining the daily link relative to the index value of the previous day \( I_{t-1} \):")
    st.latex(r"I_t = I_{t-1} \times G_t")
    st.markdown("With the base index value fixed at 100 on the first day of the index period: \( I_0 = 100 \).")
    
    # Hypothetical Example
    render_section_header("Hypothetical Calculation Example")
    st.markdown(
        """
        <div style="background-color: #ffffff; padding: 20px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
            <strong>Hypothetical Example (Single Category Match):</strong><br>
            Consider a single tracked category representative: <strong>DEL → BOM | IndiGo | 7-Day Window</strong>.
            <ul>
                <li><strong>Day 0 (Base Day)</strong>: Average fare = <strong>₹5,000</strong> (Index is set to <strong>100.00</strong>).</li>
                <li><strong>Day 1</strong>: Average fare rises to <strong>₹5,200</strong>.</li>
                <li><strong>Price Relative calculation</strong>: 
                    <code>R = 5,200 / 5,000 = 1.0400</code> (indicates a 4.00% price increase).
                </li>
                <li><strong>Link Relative</strong>: If this is the only category, the link relative <code>G_1 = 1.0400</code>.</li>
                <li><strong>Chained Index for Day 1</strong>: <code>I_1 = I_0 * G_1 = 100.00 * 1.0400 = 104.00</code>.</li>
            </ul>
            If there were another category (e.g., <strong>DEL → BLR | Air India | 15-Day Window</strong>) that went from ₹6,000 to ₹5,800:
            <ul>
                <li>Relative for Category 2: <code>R_2 = 5,800 / 6,000 = 0.9667</code>.</li>
                <li>Geometric Mean of the two relatives: <code>G_1 = √(1.0400 * 0.9667) = √1.0054 = 1.0027</code>.</li>
                <li>Chained Index for Day 1: <code>I_1 = 100.00 * 1.0027 = 100.27</code>.</li>
            </ul>
            <em style="color:#64748b;">Note: This example demonstrates how the Jevons index balances price hikes in some sectors against price drops in others.</em>
        </div>
        """,
        unsafe_allow_html=True
    )
