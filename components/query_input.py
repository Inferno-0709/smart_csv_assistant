"""
Query input component module
Contains the query input interface and tips
"""

import streamlit as st


def render_query_input():
    """Render the query input section with tips"""
    st.markdown("---")
    
    query = st.text_area(
        "💬 What would you like to analyze?",
        placeholder="Example: Calculate total FOB value by country",
        height=100
    )
    
    # Helpful tips
    with st.expander("💡 Tips for Better Results", expanded=False):
        st.markdown("""
        **Good Queries:**
        - ✅ "Calculate total FOB value by country"
        - ✅ "Find sugar exports to United Kingdom in 2025"
        - ✅ "Show top 10 countries by transaction count"
        
        **Avoid:**
        - ❌ Very complex multi-step analyses
        - ❌ Queries requiring columns that don't exist
        - ❌ Calculations on fields not present in data
        
        **Pro Tip:** Use the column reference in the sidebar to see exact column names!
        """)
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        analyze_button = st.button("🔍 Generate Code", type="primary", use_container_width=True)
    
    return query, analyze_button