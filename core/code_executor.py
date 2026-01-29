"""
Code executor module
Contains functions for safely executing generated code
"""

import pandas as pd
import sys
import io


def execute_generated_code(code, dataframes_dict):
    """
    Execute generated pandas code in a controlled environment
    
    Args:
        code: Python code to execute
        dataframes_dict: Dictionary of {df_name: dataframe} for all loaded dataframes
        
    Returns:
        Dictionary containing result, metrics, summary_text, insights, output_text, and validation_issues
    """
    # Prepare execution environment with all dataframes
    local_vars = {
        'pd': pd,
        'np': __import__('numpy')
    }
    
    # Add all dataframes to the execution environment
    for df_name, df in dataframes_dict.items():
        local_vars[df_name] = df
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        # Execute
        exec(code, {"__builtins__": __builtins__, 'pd': pd}, local_vars)
        
        sys.stdout = old_stdout
        output_text = captured_output.getvalue()
        
        # Get results
        result = local_vars.get('result', None)
        metrics = local_vars.get('metrics', {})
        summary_text = local_vars.get('summary_text', '')
        insights = local_vars.get('insights', [])
        
        # Validate results
        from utils.code_validator import validate_execution_results
        is_valid, validation_issues = validate_execution_results(result, metrics, summary_text, insights)
        
        return {
            'result': result,
            'metrics': metrics,
            'summary_text': summary_text,
            'insights': insights,
            'output_text': output_text,
            'is_valid': is_valid,
            'validation_issues': validation_issues
        }
        
    except Exception as e:
        sys.stdout = old_stdout
        # Re-raise the exception to be handled by the caller
        raise e
    finally:
        sys.stdout = old_stdout