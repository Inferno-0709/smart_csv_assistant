"""
Footer component module
Contains the application footer
"""

import streamlit as st


def render_footer():
    """Render the application footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 2rem;'>
        <strong>🛡️ Improved AI Edition with Anti-Hallucination Measures</strong><br>
        Powered by OpenAI GPT-4
    </div>
    """, unsafe_allow_html=True)