"""
LLM API handler module
Contains functions for interacting with OpenAI and Google Gemini APIs
"""

import re


def generate_code_with_openai(api_key, prompt, model="gpt-4-turbo-preview"):
    """
    Generate code using OpenAI API
    
    Args:
        api_key: OpenAI API key
        prompt: The prompt to send to the API
        model: OpenAI model to use
        
    Returns:
        Generated code as string
    """
    import openai
    
    openai.api_key = api_key
    
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a data analysis expert that generates clean, executable Python pandas code. Return only code without explanations or markdown formatting."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,  # Lower temperature for more consistent code
        max_tokens=4000
    )
    
    # Extract code
    response_text = response.choices[0].message.content
    
    # Try to extract code from markdown
    code_match = re.search(r'```(?:python)?\n(.*?)\n```', response_text, re.DOTALL)
    if code_match:
        generated_code = code_match.group(1)
    else:
        generated_code = response_text
    
    return generated_code


def generate_code_with_gemini(api_key, prompt, model="gemini-1.5-pro"):
    """
    Generate code using Google Gemini API
    
    Args:
        api_key: Google API key
        prompt: The prompt to send to the API
        model: Gemini model to use
        
    Returns:
        Generated code as string
    """
    import google.generativeai as genai
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Create model instance
    model_instance = genai.GenerativeModel(
        model_name=model,
        generation_config={
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    )
    
    # Add system instruction as part of the prompt
    full_prompt = """You are a data analysis expert that generates clean, executable Python pandas code. 
Return only code without explanations or markdown formatting.

""" + prompt
    
    # Generate response
    response = model_instance.generate_content(full_prompt)
    
    # Extract code
    response_text = response.text
    
    # Try to extract code from markdown
    code_match = re.search(r'```(?:python)?\n(.*?)\n```', response_text, re.DOTALL)
    if code_match:
        generated_code = code_match.group(1)
    else:
        generated_code = response_text
    
    return generated_code


def generate_code_with_llm(api_key, prompt, provider="openai", model=None):
    """
    Unified function to generate code using selected LLM provider
    
    Args:
        api_key: API key for the selected provider
        prompt: The prompt to send to the API
        provider: "openai" or "gemini"
        model: Specific model to use (optional, uses defaults if None)
        
    Returns:
        Generated code as string
    """
    if provider.lower() == "openai":
        model = model or "gpt-4-turbo-preview"
        return generate_code_with_openai(api_key, prompt, model)
    
    elif provider.lower() == "gemini":
        model = model or "gemini-1.5-pro"
        return generate_code_with_gemini(api_key, prompt, model)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Choose 'openai' or 'gemini'")