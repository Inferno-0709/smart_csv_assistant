"""
Sidebar component module
Contains the sidebar UI for configuration and dynamic data loading
"""

import streamlit as st
import pandas as pd


def render_sidebar():
    """Render the sidebar with configuration and dynamic file upload options"""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # LLM Provider Selection
        st.markdown("**🤖 AI Provider**")
        provider = st.selectbox(
            "Choose LLM Provider",
            options=["OpenAI", "Google Gemini"],
            help="Select which AI provider to use for code generation"
        )
        
        # Store provider in session state
        st.session_state.llm_provider = provider.lower().replace(" ", "").replace("google", "")
        
        # Model selection based on provider
        if provider == "OpenAI":
            st.markdown("**📦 Model**")
            model = st.selectbox(
                "OpenAI Model",
                options=[
                    "gpt-4-turbo-preview",
                    "gpt-4",
                    "gpt-4o",
                    "gpt-3.5-turbo"
                ],
                help="Select OpenAI model (GPT-4 recommended for best results)"
            )
            st.session_state.llm_model = model
            
            api_key = st.text_input("OpenAI API Key", type="password")
            
        else:  # Google Gemini
            st.markdown("**📦 Model**")
            model = st.selectbox(
                "Gemini Model",
                options=[
                    "gemini-1.5-pro",
                    "gemini-1.5-flash",
                    "gemini-pro"
                ],
                help="Select Gemini model (1.5 Pro recommended)"
            )
            st.session_state.llm_model = model
            
            api_key = st.text_input("Google API Key", type="password")
        
        # Show current selection
        with st.expander("ℹ️ Current AI Setup", expanded=False):
            st.write(f"**Provider:** {provider}")
            st.write(f"**Model:** {st.session_state.llm_model}")
            st.write(f"**API Key:** {'✅ Set' if api_key else '❌ Not set'}")
        
        st.markdown("---")
        st.markdown("### 📁 Upload Data Files")
        
        # Dynamic file uploader
        st.markdown("Upload as many CSV files as you need:")
        uploaded_files = st.file_uploader(
            "Choose CSV files", 
            type=['csv'],
            accept_multiple_files=True,
            help="Upload all your data files. The AI will automatically determine which files to use for your query."
        )
        
        if st.button("🚀 Load All Data", use_container_width=True):
            if uploaded_files:
                try:
                    with st.spinner("Loading data files..."):
                        # Clear existing dataframes
                        if 'dataframes' not in st.session_state:
                            st.session_state.dataframes = {}
                        
                        st.session_state.dataframes.clear()
                        
                        # Load each file
                        for file in uploaded_files:
                            # Create clean dataframe name from filename
                            df_name = file.name.replace('.csv', '').replace('-', '_').replace(' ', '_')
                            df_name = f"df_{df_name}"
                            
                            # Load the dataframe
                            df = pd.read_csv(file, low_memory=False)
                            st.session_state.dataframes[df_name] = df
                        
                        st.session_state.dataframes_loaded = True
                        st.session_state.num_files = len(uploaded_files)
                    
                    st.success(f"✅ {len(uploaded_files)} file(s) loaded successfully!")
                    
                    # Show data summary
                    with st.expander("📊 Data Summary", expanded=False):
                        for df_name, df in st.session_state.dataframes.items():
                            st.markdown(f"**{df_name}**")
                            st.write(f"- Rows: {len(df):,}")
                            st.write(f"- Columns: {len(df.columns)}")
                            st.write(f"- Preview: {', '.join(df.columns[:5].tolist())}...")
                            st.markdown("---")
                    
                except Exception as e:
                    st.error(f"❌ Error loading files: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
            else:
                st.warning("⚠️ Please upload at least one CSV file")
        
        st.markdown("---")
        
        # Show loaded files info
        if st.session_state.dataframes_loaded:
            st.markdown(f"### 📊 Loaded Files ({st.session_state.num_files})")
            
            for df_name, df in st.session_state.dataframes.items():
                with st.expander(f"🔍 {df_name}", expanded=False):
                    st.caption(f"{len(df):,} rows × {len(df.columns)} columns")
                    
                    # Show column names
                    st.markdown("**Columns:**")
                    for col in df.columns:
                        st.code(col, language=None)
            
            # Add clear data button
            if st.button("🗑️ Clear All Data", use_container_width=True):
                st.session_state.dataframes.clear()
                st.session_state.dataframes_loaded = False
                st.session_state.num_files = 0
                st.rerun()
    
    return api_key