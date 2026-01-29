"""
Configuration module for Maustats AI Analyzer
Contains page config and styling constants
"""

import streamlit as st


def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Maustats AI Analyzer - Improved",
        page_icon="📊",
        layout="wide"
    )


def apply_custom_css():
    """Apply custom CSS styling to the application"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.8rem;
            font-weight: bold;
            background: linear-gradient(90deg, #1f77b4, #2ca02c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .warning-box {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }
        .code-preview {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
            font-family: monospace;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)