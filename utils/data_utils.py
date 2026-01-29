"""
Data utilities module
Contains functions for data processing and column information extraction
"""

import pandas as pd
import numpy as np


def get_column_info(df, df_name, include_stats=True, max_unique_display=10):
    """
    Get comprehensive column information for AI prompt
    
    Args:
        df: DataFrame to analyze
        df_name: Name of the dataframe
        include_stats: Whether to include statistical information
        max_unique_display: Maximum number of unique values to display
        
    Returns:
        Detailed string with column information
    """
    info = f"\n**{df_name}** ({len(df):,} rows, {len(df.columns)} columns):\n"
    info += "=" * 80 + "\n"
    info += "EXACT Column Names (use these exactly as shown):\n\n"
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_count = df[col].isnull().sum()
        null_percent = (null_count / len(df) * 100) if len(df) > 0 else 0
        non_null_count = len(df) - null_count
        
        info += f"📊 Column: '{col}'\n"
        info += f"   - Type: {dtype}\n"
        info += f"   - Non-null: {non_null_count:,} ({100-null_percent:.1f}%), Nulls: {null_count:,} ({null_percent:.1f}%)\n"
        
        # Get sample values
        sample_values = df[col].dropna().head(5).tolist()
        info += f"   - Samples: {sample_values}\n"
        
        # Add statistics based on data type
        if include_stats:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Numeric column statistics
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    info += f"   - Range: {col_data.min():,.2f} to {col_data.max():,.2f}\n"
                    info += f"   - Mean: {col_data.mean():,.2f}, Median: {col_data.median():,.2f}\n"
                    info += f"   - Sum: {col_data.sum():,.2f}\n"
                    
                    # Check for zeros
                    zero_count = (col_data == 0).sum()
                    if zero_count > 0:
                        info += f"   - Zero values: {zero_count:,}\n"
                
            elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
                # Categorical/String column statistics
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    unique_count = col_data.nunique()
                    info += f"   - Unique values: {unique_count:,}\n"
                    
                    if unique_count <= max_unique_display:
                        # Show all unique values if not too many
                        unique_vals = col_data.unique().tolist()[:max_unique_display]
                        info += f"   - All values: {unique_vals}\n"
                    else:
                        # Show top values by frequency
                        top_values = col_data.value_counts().head(5)
                        info += f"   - Top 5 values: {dict(top_values)}\n"
                    
                    # Check for patterns
                    avg_length = col_data.astype(str).str.len().mean()
                    info += f"   - Avg length: {avg_length:.1f} characters\n"
            
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                # DateTime column statistics
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    info += f"   - Range: {col_data.min()} to {col_data.max()}\n"
                    info += f"   - Span: {(col_data.max() - col_data.min()).days} days\n"
        
        info += "\n"
    
    # Add data quality summary
    info += "=" * 80 + "\n"
    info += "DATA QUALITY SUMMARY:\n"
    total_nulls = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    completeness = ((total_cells - total_nulls) / total_cells * 100) if total_cells > 0 else 0
    info += f"- Overall completeness: {completeness:.1f}%\n"
    info += f"- Total rows: {len(df):,}\n"
    info += f"- Total columns: {len(df.columns)}\n"
    
    # Identify potential key columns
    potential_keys = []
    for col in df.columns:
        if df[col].nunique() == len(df) and df[col].notna().all():
            potential_keys.append(col)
    
    if potential_keys:
        info += f"- Potential unique identifiers: {potential_keys}\n"
    
    info += "=" * 80 + "\n\n"
    
    return info


def get_dataframe_relationships(df_transactions, df_classifications, df_enterprises):
    """
    Identify potential relationships between dataframes
    
    Returns:
        String describing potential join columns
    """
    relationships = "\n🔗 DATAFRAME RELATIONSHIPS:\n"
    relationships += "=" * 80 + "\n"
    
    # Check for common column names
    trans_cols = set(df_transactions.columns)
    class_cols = set(df_classifications.columns)
    ent_cols = set(df_enterprises.columns)
    
    # Transactions <-> Classifications
    common_trans_class = trans_cols.intersection(class_cols)
    if common_trans_class:
        relationships += f"✓ Transactions ↔ Classifications: Common columns {list(common_trans_class)}\n"
    
    # Transactions <-> Enterprises
    common_trans_ent = trans_cols.intersection(ent_cols)
    if common_trans_ent:
        relationships += f"✓ Transactions ↔ Enterprises: Common columns {list(common_trans_ent)}\n"
    
    # Classifications <-> Enterprises
    common_class_ent = class_cols.intersection(ent_cols)
    if common_class_ent:
        relationships += f"✓ Classifications ↔ Enterprises: Common columns {list(common_class_ent)}\n"
    
    relationships += "\nHINT: Use these common columns for merging/joining dataframes if needed.\n"
    relationships += "=" * 80 + "\n\n"
    
    return relationships


def analyze_dataframe_relationships(dataframes_dict):
    """
    Analyze relationships between multiple dataframes dynamically
    
    Args:
        dataframes_dict: Dictionary of {df_name: dataframe}
        
    Returns:
        String describing relationships and common columns
    """
    if len(dataframes_dict) < 2:
        return "\n🔗 DATAFRAME RELATIONSHIPS:\n" + "=" * 80 + "\nOnly one dataframe loaded - no relationships to analyze.\n" + "=" * 80 + "\n\n"
    
    relationships = "\n🔗 DATAFRAME RELATIONSHIPS:\n"
    relationships += "=" * 80 + "\n"
    
    df_names = list(dataframes_dict.keys())
    
    # Compare each pair of dataframes
    for i, df_name1 in enumerate(df_names):
        for df_name2 in df_names[i+1:]:
            df1 = dataframes_dict[df_name1]
            df2 = dataframes_dict[df_name2]
            
            # Find common columns
            common_cols = set(df1.columns).intersection(set(df2.columns))
            
            if common_cols:
                relationships += f"\n✓ {df_name1} ↔ {df_name2}:\n"
                relationships += f"  Common columns: {list(common_cols)}\n"
                
                # Check if common columns could be join keys (high uniqueness)
                potential_keys = []
                for col in common_cols:
                    # Check uniqueness ratio in both dataframes
                    if len(df1) > 0 and len(df2) > 0:
                        uniqueness1 = df1[col].nunique() / len(df1)
                        uniqueness2 = df2[col].nunique() / len(df2)
                        
                        if uniqueness1 > 0.9 or uniqueness2 > 0.9:
                            potential_keys.append(col)
                
                if potential_keys:
                    relationships += f"  Potential join keys: {potential_keys}\n"
    
    relationships += "\n💡 HINT: Use common columns for merging/joining dataframes if needed.\n"
    relationships += "=" * 80 + "\n\n"
    
    return relationships


def analyze_query_relevance(query, dataframes_dict):
    """
    Analyze which dataframes are most relevant to the user's query
    
    Args:
        query: User's query string
        dataframes_dict: Dictionary of {df_name: dataframe}
        
    Returns:
        List of relevant dataframe names sorted by relevance
    """
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    relevance_scores = {}
    
    for df_name, df in dataframes_dict.items():
        score = 0
        
        # Check if dataframe name is mentioned in query
        clean_df_name = df_name.replace('df_', '').replace('_', ' ').lower()
        if clean_df_name in query_lower:
            score += 100
        
        # Check column name matches
        for col in df.columns:
            col_lower = col.lower()
            col_words = set(col_lower.replace('_', ' ').split())
            
            # Exact column name match
            if col_lower in query_lower:
                score += 50
            
            # Word overlap
            word_overlap = len(query_words.intersection(col_words))
            score += word_overlap * 10
            
            # Check for semantic similarity (basic keyword matching)
            keywords_map = {
                'country': ['country', 'nation', 'destination', 'origin'],
                'product': ['product', 'item', 'commodity', 'goods', 'hs', 'classification'],
                'value': ['value', 'amount', 'price', 'fob', 'cost', 'total'],
                'date': ['date', 'time', 'year', 'month', 'period'],
                'quantity': ['quantity', 'volume', 'weight', 'units'],
                'enterprise': ['enterprise', 'company', 'business', 'firm', 'exporter', 'importer']
            }
            
            for keyword, synonyms in keywords_map.items():
                if any(syn in query_lower for syn in synonyms):
                    if any(syn in col_lower for syn in synonyms):
                        score += 20
        
        # Check data type relevance
        if 'total' in query_lower or 'sum' in query_lower or 'calculate' in query_lower:
            numeric_cols = df.select_dtypes(include=['number']).columns
            score += len(numeric_cols) * 5
        
        relevance_scores[df_name] = score
    
    # Sort by relevance score
    sorted_dfs = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Return dataframes with score > 0, or all if none match
    relevant_dfs = [df_name for df_name, score in sorted_dfs if score > 0]
    
    if not relevant_dfs:
        # Return all dataframes if no clear match
        relevant_dfs = list(dataframes_dict.keys())
    
    return relevant_dfs