"""
Maustats AI Analyzer - Main Application
A Streamlit application for AI-powered data analysis with anti-hallucination measures
Now with dynamic multi-file support!
"""

import streamlit as st

# Configuration imports
from config.page_config import setup_page_config, apply_custom_css
from config.session_state import initialize_session_state

# Component imports
from components.sidebar import render_sidebar
from components.header import render_header, render_welcome_screen
from components.query_input import render_query_input
from components.code_review import render_code_review
from components.results_display import render_results, render_error
from components.footer import render_footer

# Core functionality imports
from core.llm_handler import generate_code_with_llm
from core.code_executor import execute_generated_code

# Utility imports
from utils.data_utils import (
    get_column_info, 
    analyze_dataframe_relationships,
    analyze_query_relevance
)
from utils.code_validator import validate_code
from utils.prompt_generator import generate_improved_prompt


def main():
    """Main application entry point"""
    
    # Setup
    setup_page_config()
    apply_custom_css()
    initialize_session_state()
    
    # Render sidebar and get API key
    api_key = render_sidebar()
    
    # Render header
    render_header()
    
    # Main content logic
    if not st.session_state.dataframes_loaded:
        render_welcome_screen()
    else:
        # Render query input
        query, analyze_button = render_query_input()
        
        # Handle code generation
        if analyze_button and query:
            if not api_key:
                provider_name = st.session_state.llm_provider.upper()
                st.error(f"❌ Please enter your {provider_name} API Key in the sidebar")
            else:
                try:
                    with st.spinner(f"🤔 Analyzing query using {st.session_state.llm_provider.upper()} ({st.session_state.llm_model})..."):
                        # Get all dataframes
                        dataframes_dict = st.session_state.dataframes
                        
                        # Analyze which dataframes are most relevant to the query
                        relevant_df_names = analyze_query_relevance(query, dataframes_dict)
                        
                        # Show which files are being used
                        st.info(f"🎯 **Relevant dataframes identified:** {', '.join(relevant_df_names)}")
                        
                        # Build comprehensive data context for AI
                        df_info = ""
                        df_info += f"\n{'='*80}\n"
                        df_info += f"📊 AVAILABLE DATAFRAMES ({len(dataframes_dict)} total)\n"
                        df_info += f"{'='*80}\n"
                        
                        # Add info for relevant dataframes (primary focus)
                        df_info += f"\n🎯 PRIMARY DATAFRAMES (Most relevant to query):\n\n"
                        for df_name in relevant_df_names[:3]:  # Top 3 most relevant
                            if df_name in dataframes_dict:
                                df_info += get_column_info(
                                    dataframes_dict[df_name], 
                                    df_name, 
                                    include_stats=True
                                )
                        
                        # Add brief info for other dataframes (available but less relevant)
                        other_dfs = [name for name in dataframes_dict.keys() if name not in relevant_df_names[:3]]
                        if other_dfs:
                            df_info += f"\n📋 OTHER AVAILABLE DATAFRAMES:\n"
                            for df_name in other_dfs:
                                df = dataframes_dict[df_name]
                                df_info += f"\n- {df_name}: {len(df):,} rows, {len(df.columns)} columns\n"
                                df_info += f"  Columns: {', '.join(df.columns[:10].tolist())}"
                                if len(df.columns) > 10:
                                    df_info += f" ... ({len(df.columns)} total)"
                                df_info += "\n"
                        
                        # Add dataframe relationships
                        df_info += analyze_dataframe_relationships(dataframes_dict)
                        
                        # Generate improved prompt
                        prompt = generate_improved_prompt(query, df_info)
                        
                        # Generate code using selected LLM
                        generated_code = generate_code_with_llm(
                            api_key=api_key,
                            prompt=prompt,
                            provider=st.session_state.llm_provider,
                            model=st.session_state.llm_model
                        )
                        
                        # Store in session state
                        st.session_state.generated_code = generated_code
                        st.session_state.code_validated = False
                    
                    st.success(f"✅ Code generated using {st.session_state.llm_provider.upper()}! Please review below before executing.")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating code with {st.session_state.llm_provider.upper()}: {str(e)}")
                    st.exception(e)
        
        # Show generated code and validation
        if hasattr(st.session_state, 'generated_code'):
            # Validate code with all available dataframe names
            available_dfs = list(st.session_state.dataframes.keys())
            validation_issues = validate_code(st.session_state.generated_code, available_dfs)
            
            # Render code review
            execute_button, discard_button = render_code_review(
                st.session_state.generated_code,
                validation_issues
            )
            
            # Handle discard
            if discard_button:
                del st.session_state.generated_code
                st.rerun()
            
            # Handle execution
            if execute_button:
                try:
                    with st.spinner("⚙️ Executing code..."):
                        execution_results = execute_generated_code(
                            st.session_state.generated_code,
                            st.session_state.dataframes
                        )
                    
                    # Display results
                    render_results(execution_results)
                    
                    # Clean up
                    del st.session_state.generated_code
                    
                except Exception as e:
                    render_error(e)
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()