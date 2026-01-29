"""
Code review component module
Contains UI for code validation and review
"""

import streamlit as st


def render_code_review(generated_code, validation_issues):
    """
    Render the code review section with validation results
    
    Args:
        generated_code: The generated code to review
        validation_issues: List of validation issues found
        
    Returns:
        Tuple of (execute_button, discard_button) states
    """
    st.markdown("---")
    st.markdown("### 🔍 Generated Code Review")
    
    # Show validation results
    if validation_issues:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**⚠️ Potential Issues Detected:**")
        for issue in validation_issues:
            st.markdown(f"- {issue}")
        st.markdown("Review the code carefully before executing!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Code validation passed - no obvious issues detected")
    
    # Show code
    st.markdown("**📝 Generated Code:**")
    st.code(generated_code, language='python')
    
    # Execution buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        execute_button = st.button("▶️ Execute Code", type="primary", use_container_width=True)
    
    with col2:
        discard_button = st.button("🗑️ Discard", use_container_width=True)
    
    return execute_button, discard_button