# CSV AI Analyzer

A powerful, Streamlit-based application for AI-powered data analysis. This tool leverages Large Language Models (LLMs) like Google Gemini and OpenAI to generate Python code for analyzing CSV and Excel files, complete with anti-hallucination measures and dynamic multi-file support.

## 🚀 Features

- **Dynamic Multi-File Support**: Upload and analyze multiple CSV or Excel files simultaneously.
- **AI-Powered Analysis**: Uses advanced LLMs (Google Gemini, OpenAI GPT-4) to understand data structure and user queries.
- **Automated Code Generation**: translate natural language questions into executable Python/Pandas code.
- **Anti-Hallucination**: Built-in code validation to ensure generated code uses correct column names and follows data logic.
- **Interactive Code Review**: Review, edit, and execution control over the generated code before running it.
- **Smart Context Awareness**: Automatically identifies relevant dataframes and relationships based on your query.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd "Smart CSV assistant"
    ```

2.  **Install Dependencies**
    Ensure you have Python installed (3.8+ recommended). Install the required packages:
    ```bash
    pip install streamlit pandas numpy google-generativeai openai
    ```

3.  **API Configuration**
    You will need an API key from either:
    - [Google AI Studio](https://aistudio.google.com/) (for Gemini)
    - [OpenAI Platform](https://platform.openai.com/) (for GPT models)

## 🏃 Usage

1.  **Start the Application**
    Run the Streamlit app from the project root:
    ```bash
    streamlit run analyzer/app.py
    ```

2.  **Using the App**
    - **Sidebar**: Enter your API Key (Gemini or OpenAI).
    - **Upload**: Drag and drop your CSV or Excel files into the file uploader.
    - **Query**: Type your question about the data (e.g., "What is the total sales by region?", "Compare the average price between 2023 and 2024").
    - **Review**: The AI will generate code. Review it in the code editor.
    - **Execute**: Click "Execute Code" to run the analysis and see the results (tables, charts, validation).

## 📂 Project Structure

- `analyzer/`
    - `app.py`: Main entry point for the Streamlit application.
    - `components/`: UI components (Sidebar, Header, Query Input, Results Display).
    - `core/`: Core logic for LLM interaction (`llm_handler.py`) and code execution (`code_executor.py`).
    - `config/`: Application configuration and session state management.
    - `utils/`: Helper utilities for data processing (`data_utils.py`), code validation, and prompt generation.

## ⚠️ Note

This tool executes generated Python code. While it includes validation steps, always review the code before execution, especially when working with sensitive data or production environments.
