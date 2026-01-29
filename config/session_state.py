"""
Session state management module
Handles initialization and management of Streamlit session state
"""

import streamlit as st


def initialize_session_state():
    """Initialize session state variables for dynamic multi-file system"""
    if 'dataframes_loaded' not in st.session_state:
        st.session_state.dataframes_loaded = False
    
    if 'dataframes' not in st.session_state:
        st.session_state.dataframes = {}  # Dictionary to store multiple dataframes
    
    if 'num_files' not in st.session_state:
        st.session_state.num_files = 0
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # LLM configuration
    if 'llm_provider' not in st.session_state:
        st.session_state.llm_provider = 'openai'  # Default to OpenAI
    
    if 'llm_model' not in st.session_state:
        st.session_state.llm_model = 'gpt-4-turbo-preview'  # Default model