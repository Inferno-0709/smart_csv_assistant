"""
Results display component module
Contains UI for displaying analysis results
"""

import streamlit as st
import pandas as pd
from datetime import datetime


def render_results(execution_results):
    """
    Render the analysis results with quality indicators
    
    Args:
        execution_results: Dictionary containing result, metrics, summary_text, insights, output_text, 
                          is_valid, and validation_issues
    """
    result = execution_results['result']
    metrics = execution_results['metrics']
    summary_text = execution_results['summary_text']
    insights = execution_results['insights']
    output_text = execution_results['output_text']
    is_valid = execution_results.get('is_valid', True)
    validation_issues = execution_results.get('validation_issues', [])
    
    st.markdown("---")
    st.markdown("### ✅ Results")
    
    # Show validation warnings if any
    if validation_issues:
        with st.expander("⚠️ Quality Warnings", expanded=True):
            st.warning("The code executed successfully, but there are some quality concerns:")
            for issue in validation_issues:
                st.markdown(f"- {issue}")
    
    # Quality Score
    quality_score = calculate_quality_score(metrics, insights, summary_text, result)
    
    # Display quality indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("**📊 Analysis Quality Score**")
    with col2:
        color = "green" if quality_score >= 80 else "orange" if quality_score >= 60 else "red"
        st.markdown(f"<h2 style='color: {color}; margin: 0;'>{quality_score}/100</h2>", unsafe_allow_html=True)
    with col3:
        if quality_score >= 80:
            st.success("Excellent ✨")
        elif quality_score >= 60:
            st.warning("Good 👍")
        else:
            st.error("Needs work 🔧")
    
    st.markdown("---")
    
    # Summary
    if summary_text:
        st.info(f"**📋 Summary:** {summary_text}")
    else:
        st.warning("⚠️ No summary provided")
    
    # Metrics
    if metrics:
        st.markdown("**📊 Key Metrics:**")
        
        # Show metrics in a nice grid
        metric_items = list(metrics.items())
        num_cols = min(len(metric_items), 4)
        
        if num_cols > 0:
            rows_needed = (len(metric_items) + num_cols - 1) // num_cols
            
            for row in range(rows_needed):
                cols = st.columns(num_cols)
                for col_idx in range(num_cols):
                    metric_idx = row * num_cols + col_idx
                    if metric_idx < len(metric_items):
                        key, value = metric_items[metric_idx]
                        with cols[col_idx]:
                            formatted_value = format_metric_value(value)
                            st.metric(
                                label=key.replace('_', ' ').title(),
                                value=formatted_value,
                                help=f"Raw value: {value}"
                            )
        
        # Show completeness indicator
        metrics_count = len(metrics)
        if metrics_count >= 5:
            st.success(f"✅ {metrics_count} metrics provided (comprehensive)")
        else:
            st.warning(f"⚠️ Only {metrics_count} metrics provided (recommended: 5+)")
    else:
        st.error("❌ No metrics provided")
    
    # Data
    if result is not None:
        st.markdown("**📋 Data Results:**")
        
        if isinstance(result, pd.DataFrame):
            # Show data statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", f"{len(result):,}")
            with col2:
                st.metric("Columns", len(result.columns))
            with col3:
                # Calculate data completeness
                if len(result) > 0:
                    completeness = (1 - result.isnull().sum().sum() / (len(result) * len(result.columns))) * 100
                    st.metric("Completeness", f"{completeness:.1f}%")
            
            # Show the dataframe
            st.dataframe(result, use_container_width=True, height=400)
            
            # Download button
            csv = result.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=False
            )
        else:
            st.write(result)
    else:
        st.error("❌ No result data provided")
    
    # Console Output
    if output_text:
        with st.expander("📝 Console Output"):
            st.code(output_text, language='text')
    
    # Insights
    if insights:
        st.markdown("**💡 Key Insights:**")
        
        insights_count = len(insights)
        if insights_count >= 5:
            st.success(f"✅ {insights_count} insights provided (comprehensive)")
        else:
            st.warning(f"⚠️ Only {insights_count} insights provided (recommended: 5+)")
        
        for idx, insight in enumerate(insights, 1):
            # Check if insight contains numbers (good sign)
            has_numbers = any(char.isdigit() for char in str(insight))
            icon = "✅" if has_numbers else "ℹ️"
            st.markdown(f"{icon} **{idx}.** {insight}")
    else:
        st.error("❌ No insights provided")
    
    # Overall success message
    if quality_score >= 80:
        st.success("✅ Analysis completed successfully with high quality results!")
    elif quality_score >= 60:
        st.info("ℹ️ Analysis completed. Consider regenerating for more comprehensive insights.")
    else:
        st.warning("⚠️ Analysis completed but quality could be improved. Try regenerating with a more specific query.")


def format_metric_value(value):
    """Format metric values for display"""
    if isinstance(value, (int, float)):
        if abs(value) > 1_000_000:
            return f"${value/1_000_000:.2f}M"
        elif abs(value) > 1_000:
            return f"{value:,.0f}"
        else:
            return f"{value:.2f}"
    else:
        # Truncate long strings
        str_value = str(value)
        if len(str_value) > 30:
            return str_value[:27] + "..."
        return str_value


def calculate_quality_score(metrics, insights, summary_text, result):
    """
    Calculate a quality score for the analysis results
    
    Returns: Score from 0-100
    """
    score = 0
    
    # Metrics quality (30 points)
    if metrics:
        metrics_count = len(metrics)
        if metrics_count >= 5:
            score += 30
        else:
            score += metrics_count * 6  # 6 points per metric up to 5
    
    # Insights quality (30 points)
    if insights:
        insights_count = len(insights)
        if insights_count >= 5:
            score += 20
        else:
            score += insights_count * 4  # 4 points per insight up to 5
        
        # Bonus for insights with numbers
        insights_with_numbers = sum(1 for insight in insights if any(char.isdigit() for char in str(insight)))
        score += min(10, insights_with_numbers * 2)
    
    # Summary quality (20 points)
    if summary_text:
        if len(summary_text) >= 100:
            score += 20
        else:
            score += len(summary_text) / 5  # Proportional to length
    
    # Result data quality (20 points)
    if result is not None:
        if isinstance(result, pd.DataFrame):
            if len(result) > 0:
                score += 15
                # Bonus for multiple columns
                if len(result.columns) > 1:
                    score += 5
            else:
                score += 5  # Some points for empty but valid result
        else:
            score += 10  # Non-DataFrame result
    
    return min(100, int(score))


def render_error(error):
    """
    Render error message with debugging help
    
    Args:
        error: Exception object
    """
    st.error(f"❌ Error executing code: {str(error)}")
    
    st.markdown("**🐛 Debugging Help:**")
    st.markdown("""
    This error might be due to:
    1. **Wrong column names** - Check the column reference in sidebar
    2. **Data type mismatch** - Verify column types match operations
    3. **Missing data** - Some fields might be empty
    4. **Division by zero** - Check for empty groups or zero values
    5. **Index out of bounds** - Result might be empty
    
    Try:
    - Simplifying your query
    - Being more specific about column names
    - Checking that columns exist in your data
    - Asking for a different analysis approach
    """)
    
    # Provide specific suggestions based on error type
    error_str = str(error).lower()
    
    if 'keyerror' in error_str or 'column' in error_str:
        st.warning("💡 **Suggestion**: This looks like a column name issue. Check the exact column names in the sidebar.")
    elif 'indexerror' in error_str or 'iloc' in error_str:
        st.warning("💡 **Suggestion**: The result might be empty. Try a less restrictive query.")
    elif 'typeerror' in error_str:
        st.warning("💡 **Suggestion**: There might be a data type mismatch. Check if you're comparing compatible types.")
    elif 'zerodivision' in error_str:
        st.warning("💡 **Suggestion**: Division by zero occurred. The data might not contain the expected values.")
    
    with st.expander("🔍 Full Error Details"):
        st.exception(error)