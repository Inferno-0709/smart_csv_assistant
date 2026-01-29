"""
Prompt generation module
Contains functions for generating AI prompts
"""


def generate_improved_prompt(query, df_info):
    """Generate a robust prompt with strict requirements to ensure complete and accurate outputs"""
    
    prompt = f"""You are an expert data analyst. Generate Python pandas code to comprehensively answer this query.

**USER QUERY**: "{query}"

{df_info}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  CRITICAL REQUIREMENTS - FAILURE TO FOLLOW WILL RESULT IN REJECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. **COLUMN NAMES**: Use ONLY the EXACT column names listed above (copy-paste verbatim)
   - Never guess or invent column names
   - Never use columns not explicitly listed
   - Use bracket notation if column names have spaces: df['Column Name']

2. **TEXT FILTERING**: 
   - ALWAYS use .str.contains(pattern, case=False, na=False) for text filtering
   - NEVER use == for partial text matching
   - Handle null values with na=False parameter

3. **NULL HANDLING**:
   - Check for nulls before operations: .notna() or .dropna()
   - Use fillna() where appropriate
   - Never assume data is complete

4. **DATA VALIDATION**:
   - Add checks for empty dataframes: if len(df) == 0
   - Handle edge cases (division by zero, empty groups)
   - Use .get() for dictionary access with defaults

5. **BOOLEAN OPERATIONS**:
   - Wrap ALL conditions in parentheses when using & or |
   - Example: df[(df['Col1'] > 5) & (df['Col2'].str.contains('text', na=False))]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MANDATORY OUTPUT FORMAT - ALL 4 VARIABLES REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You MUST create these 4 variables with the EXACT names:

```python
# 1. RESULT (REQUIRED)
result = ...  # DataFrame or Series with the main analysis result
              # Must be properly formatted with clear column names

# 2. METRICS (REQUIRED - minimum 5 metrics)
metrics = {{
    'total_count': ...,           # Total number of records
    'total_value': ...,            # Sum of main value column (if applicable)
    'average_value': ...,          # Average of main value (if applicable)
    'unique_count': ...,           # Number of unique categories/groups
    'top_item': ...,               # Name of top item by value
    'top_item_value': ...,         # Value of top item
    'percentage_of_top': ...,      # % that top item represents
    # Add 2-3 more relevant metrics specific to the query
}}

# 3. SUMMARY_TEXT (REQUIRED)
summary_text = "Comprehensive 3-4 sentence summary that:
1. States the main finding with specific numbers
2. Mentions the top item/category with its value
3. Provides context (percentage, comparison)
4. Notes any important patterns or anomalies"

# 4. INSIGHTS (REQUIRED - minimum 5 insights)
insights = [
    "Insight 1: Specific finding with exact numbers and percentages",
    "Insight 2: Comparison or trend with calculations shown",
    "Insight 3: Distribution pattern with supporting stats",
    "Insight 4: Notable outlier or anomaly with impact assessment",
    "Insight 5: Actionable recommendation based on the data",
    # Add more if relevant to the query
]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ QUALITY CHECKLIST - VERIFY BEFORE SUBMITTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ All 4 output variables created (result, metrics, summary_text, insights)
□ At least 5 meaningful metrics calculated
□ At least 5 specific insights with numbers
□ All column names match exactly
□ Null values handled properly
□ Edge cases covered (empty data, division by zero)
□ Text filtering uses .str.contains() with na=False
□ Boolean operations properly parenthesized
□ Result has clear, descriptive column names
□ Summary and insights reference specific calculated values

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 COMPREHENSIVE EXAMPLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query: "Calculate total FOB by country and show top performers"

```python
import pandas as pd
import numpy as np

# Ensure column exists and handle nulls
if 'Country' not in df_transactions.columns or 'Free On Board' not in df_transactions.columns:
    raise ValueError("Required columns not found")

# Filter out nulls
df_clean = df_transactions[df_transactions['Country'].notna() & df_transactions['Free On Board'].notna()].copy()

# Calculate totals by country
result = df_clean.groupby('Country')['Free On Board'].agg([
    ('Total_FOB', 'sum'),
    ('Transaction_Count', 'count'),
    ('Average_FOB', 'mean')
]).reset_index()

# Sort by total FOB descending
result = result.sort_values('Total_FOB', ascending=False).reset_index(drop=True)

# Calculate metrics
total_fob = result['Total_FOB'].sum()
total_countries = len(result)
total_transactions = result['Transaction_Count'].sum()

# Handle empty results
if total_countries > 0:
    top_country = result.iloc[0]['Country']
    top_country_fob = result.iloc[0]['Total_FOB']
    top_country_pct = (top_country_fob / total_fob * 100) if total_fob > 0 else 0
    
    # Calculate concentration metrics
    top_5_fob = result.head(5)['Total_FOB'].sum() if len(result) >= 5 else total_fob
    top_5_concentration = (top_5_fob / total_fob * 100) if total_fob > 0 else 0
    
    avg_fob_per_country = total_fob / total_countries if total_countries > 0 else 0
    
else:
    top_country = "N/A"
    top_country_fob = 0
    top_country_pct = 0
    top_5_concentration = 0
    avg_fob_per_country = 0

metrics = {{
    'total_countries': total_countries,
    'total_fob': round(total_fob, 2),
    'total_transactions': int(total_transactions),
    'average_fob_per_country': round(avg_fob_per_country, 2),
    'top_country': str(top_country),
    'top_country_fob': round(top_country_fob, 2),
    'top_country_percentage': round(top_country_pct, 2),
    'top_5_concentration': round(top_5_concentration, 2),
    'avg_transaction_value': round(total_fob / total_transactions, 2) if total_transactions > 0 else 0
}}

summary_text = f"Analysis of {{total_countries:,}} countries reveals total FOB value of ${{total_fob:,.2f}} across {{total_transactions:,}} transactions. {{top_country}} dominates with ${{top_country_fob:,.2f}} ({{top_country_pct:.1f}}% of total). The top 5 countries account for {{top_5_concentration:.1f}}% of all exports, indicating {{('high' if top_5_concentration > 70 else 'moderate')}} market concentration."

insights = [
    f"{{top_country}} is the leading export destination with ${{top_country_fob:,.2f}}, representing {{top_country_pct:.1f}}% of total FOB value",
    f"Average FOB per country is ${{avg_fob_per_country:,.2f}}, with {{top_country}} performing {{(top_country_fob/avg_fob_per_country):.1f}}x above average",
    f"Top 5 countries control {{top_5_concentration:.1f}}% of export value, indicating {{('high concentration risk' if top_5_concentration > 70 else 'diversified market presence')}}",
    f"Average transaction value is ${{(total_fob/total_transactions):,.2f}}, suggesting {{('large-scale' if (total_fob/total_transactions) > 100000 else 'mixed-scale')}} operations",
    f"With {{total_countries}} active destinations, the market shows {{('strong' if total_countries > 50 else 'limited')}} geographic diversification"
]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 YOUR TASK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate code for the user's query following ALL requirements above.

CRITICAL: 
- Include ALL error handling (null checks, empty data, division by zero)
- Create MINIMUM 5 metrics with descriptive names
- Create MINIMUM 5 insights with specific numbers and calculations
- Use exact column names from the data info
- Return ONLY executable Python code with NO markdown formatting
- Do NOT include explanatory text, only code

Begin your response with: import pandas as pd
"""
    
    return prompt