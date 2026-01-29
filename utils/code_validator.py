"""
Code validation module
Contains functions for validating generated code
"""

import ast
import re


def validate_code(code, available_dfs):
    """
    Comprehensive validation of generated code
    
    Args:
        code: Python code string to validate
        available_dfs: List of available dataframe names
        
    Returns:
        List of validation issues found
    """
    issues = []
    warnings = []
    
    # ============================================================================
    # SECURITY CHECKS
    # ============================================================================
    
    # Check for dangerous imports
    dangerous_imports = ['os', 'sys', 'subprocess', 'eval', 'exec', 'compile', '__import__']
    for imp in dangerous_imports:
        if f'import {imp}' in code or f'from {imp}' in code:
            issues.append(f"🚫 SECURITY: Code tries to import '{imp}' (not allowed)")
    
    if 'import openai' in code or 'from openai' in code:
        issues.append("🚫 Code tries to import openai (not allowed)")
    
    # Check for file operations
    if 'open(' in code or 'write(' in code or 'read(' in code:
        issues.append("🚫 SECURITY: Code tries to perform file operations (not allowed)")
    
    # Check for network operations
    if 'requests.' in code or 'urllib' in code or 'socket' in code:
        issues.append("🚫 SECURITY: Code tries to make network requests (not allowed)")
    
    # ============================================================================
    # DATAFRAME USAGE CHECKS
    # ============================================================================
    
    # Check if code uses at least one available dataframe
    uses_any_df = False
    for df_name in available_dfs:
        if df_name in code:
            uses_any_df = True
            break
    
    if not uses_any_df:
        issues.append("⚠️ CRITICAL: Code doesn't use any of the available dataframes")
    
    # Note which dataframes are used
    used_dfs = [df_name for df_name in available_dfs if df_name in code]
    unused_dfs = [df_name for df_name in available_dfs if df_name not in code]
    
    if used_dfs:
        warnings.append(f"ℹ️ Using dataframes: {', '.join(used_dfs)}")
    
    if unused_dfs and len(used_dfs) > 0:
        warnings.append(f"ℹ️ Not using: {', '.join(unused_dfs)} (this might be intentional based on the query)")
    
    # ============================================================================
    # REQUIRED OUTPUT CHECKS
    # ============================================================================
    
    # Check for required output variables
    required_vars = ['result', 'metrics', 'summary_text', 'insights']
    missing_vars = []
    
    for var in required_vars:
        # Look for variable assignment patterns
        if not re.search(rf'\b{var}\s*=', code):
            missing_vars.append(var)
    
    if missing_vars:
        issues.append(f"⚠️ CRITICAL: Missing required output variables: {', '.join(missing_vars)}")
    
    # Check metrics structure
    if 'metrics' in code and 'metrics = {' in code:
        # Try to count the number of metrics
        metrics_match = re.search(r'metrics\s*=\s*\{([^}]+)\}', code, re.DOTALL)
        if metrics_match:
            metrics_content = metrics_match.group(1)
            # Count key-value pairs (rough estimate)
            metric_count = metrics_content.count(':')
            if metric_count < 5:
                warnings.append(f"⚠️ QUALITY: Only {metric_count} metrics found, recommend at least 5 for comprehensive analysis")
    
    # Check insights structure
    if 'insights' in code and 'insights = [' in code:
        insights_match = re.search(r'insights\s*=\s*\[([^\]]+)\]', code, re.DOTALL)
        if insights_match:
            insights_content = insights_match.group(1)
            # Count insights (rough estimate)
            insight_count = insights_content.count('"') // 2 + insights_content.count("'") // 2
            if insight_count < 5:
                warnings.append(f"⚠️ QUALITY: Only {insight_count} insights found, recommend at least 5 for thorough analysis")
    
    # ============================================================================
    # DATA HANDLING CHECKS
    # ============================================================================
    
    # Check for null handling
    if '.str.' in code and 'na=False' not in code:
        warnings.append("⚠️ WARNING: String operations found but 'na=False' not used - may cause issues with null values")
    
    # Check for proper boolean operations
    if ('&' in code or '|' in code) and not re.search(r'\([^)]+\)\s*[&|]\s*\([^)]+\)', code):
        warnings.append("⚠️ WARNING: Boolean operations found but conditions may not be properly parenthesized")
    
    # Check for division operations that might cause division by zero
    if '/' in code and 'if ' not in code.lower():
        warnings.append("ℹ️ NOTE: Division operations found - ensure zero-division is handled")
    
    # Check for .iloc or .loc without bounds checking
    if ('.iloc[0]' in code or '.loc[0]' in code) and 'if len(' not in code:
        warnings.append("⚠️ WARNING: Direct indexing found without checking if data exists - may fail on empty results")
    
    # ============================================================================
    # SYNTAX CHECKS (using AST)
    # ============================================================================
    
    try:
        ast.parse(code)
    except SyntaxError as e:
        issues.append(f"🚫 SYNTAX ERROR: {str(e)}")
    except Exception as e:
        warnings.append(f"⚠️ Could not parse code: {str(e)}")
    
    # ============================================================================
    # BEST PRACTICES CHECKS
    # ============================================================================
    
    # Check for hardcoded values that should be dynamic
    if re.search(r'\[\d+\]', code) and 'len(' not in code:
        warnings.append("ℹ️ NOTE: Hardcoded indices found - ensure they're within bounds")
    
    # Check for proper column name usage (with quotes)
    if "df['" not in code and 'df["' not in code and any(df in code for df in available_dfs):
        warnings.append("ℹ️ NOTE: Ensure column names are accessed with quotes: df['column_name']")
    
    # Combine issues and warnings
    all_issues = issues + warnings
    
    return all_issues


def validate_execution_results(result, metrics, summary_text, insights):
    """
    Validate the results after code execution
    
    Args:
        result: The result DataFrame/Series
        metrics: Dictionary of metrics
        summary_text: Summary string
        insights: List of insights
        
    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []
    is_valid = True
    
    # Check result
    if result is None:
        issues.append("❌ Result is None")
        is_valid = False
    elif hasattr(result, '__len__') and len(result) == 0:
        issues.append("⚠️ Result is empty - query may have found no matching data")
    
    # Check metrics
    if not metrics:
        issues.append("❌ Metrics dictionary is empty")
        is_valid = False
    elif len(metrics) < 5:
        issues.append(f"⚠️ Only {len(metrics)} metrics provided, recommended minimum is 5")
    
    # Check for None values in metrics
    if metrics:
        none_metrics = [k for k, v in metrics.items() if v is None]
        if none_metrics:
            issues.append(f"⚠️ Metrics contain None values: {', '.join(none_metrics)}")
    
    # Check summary_text
    if not summary_text or summary_text.strip() == "":
        issues.append("❌ Summary text is empty")
        is_valid = False
    elif len(summary_text) < 50:
        issues.append("⚠️ Summary text is very short (less than 50 characters)")
    
    # Check insights
    if not insights:
        issues.append("❌ Insights list is empty")
        is_valid = False
    elif len(insights) < 5:
        issues.append(f"⚠️ Only {len(insights)} insights provided, recommended minimum is 5")
    
    # Check if insights contain actual numbers
    if insights:
        insights_with_numbers = sum(1 for insight in insights if any(char.isdigit() for char in str(insight)))
        if insights_with_numbers < len(insights) * 0.6:  # At least 60% should have numbers
            issues.append("⚠️ Many insights lack specific numbers - they should include concrete data")
    
    return is_valid, issues