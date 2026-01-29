"""
Header component module
Contains the main header and welcome screen
"""

import streamlit as st


def render_header():
    """Render the main header"""
    st.markdown('<div class="main-header">📊 CSV AI Analyzer - UNIVERSAL</div>', unsafe_allow_html=True)
    st.markdown("### Multi-LLM Support | OpenAI & Google Gemini")


def render_welcome_screen():
    """Render the welcome screen when no data is loaded"""
    st.info("👈 **Upload your data files in the sidebar to get started**")
    
    st.markdown("""
    ### ✨ Features in This Version:
    
    1. **🎯 Dynamic Multi-File Upload** - Upload any number of CSV files (NEW!)
    2. **🤖 Intelligent Query Routing** - AI automatically selects relevant files (NEW!)
    3. **📋 Exact Column Names** - AI sees your exact column names with data types
    4. **✅ Code Validation** - Checks generated code before execution
    5. **👁️ Code Preview** - Review code before running
    6. **🔍 Column Reference** - Quick access to exact column names
    7. **⚠️ Better Error Handling** - Clear error messages
    8. **📊 Sample Data** - AI sees sample values from your data
    9. **🔗 Relationship Detection** - Automatically identifies common columns (NEW!)
    10. **💯 Quality Scoring** - 0-100 score for result quality
    
    ### 🆕 How Multi-File Works:
    
    - Upload **any number** of CSV files (not limited to 3!)
    - Each file becomes a dataframe (e.g., `df_sales.csv` → `df_sales`)
    - AI **analyzes your query** and determines which files are relevant
    - AI **automatically uses** the most appropriate dataframes
    - You can still reference specific files in your query if needed
    
    ### 📝 Example Queries:
    
    - "Show total sales by region" → AI uses sales-related files
    - "Analyze customer demographics" → AI uses customer files
    - "Compare product performance across stores" → AI uses product + store files
    - "Join sales and inventory data" → AI uses both and identifies join columns
    
    This significantly reduces complexity and improves accuracy!
    """)