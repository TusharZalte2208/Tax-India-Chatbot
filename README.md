# TaxBot India

A Streamlit-based Income Tax Chatbot that calculates and compares Indian tax regimes, provides tax-saving suggestions, and generates downloadable PDF reports with a dark-themed UI.

## Features

- 💰 Calculate taxes under both old and new Indian tax regimes
- 📊 Compare tax liabilities between regimes
- 💡 Get personalized tax-saving recommendations
- 📄 Generate detailed PDF tax reports
- 🌙 Dark-themed responsive UI

## Installation

1. Extract the `taxbot_india.zip` file
2. Install the required dependencies:

```bash
pip install streamlit fpdf
```

3. Run the application:

```bash
streamlit run main.py
```

## Usage

1. Enter your income and deduction details in the form
2. Click the "Calculate Tax" button
3. View the comparison between tax regimes
4. Get personalized tax-saving recommendations
5. Download a detailed PDF report for your records

## Files

- `main.py` - The main Streamlit application file
- `tax_calculator.py` - Tax calculation logic and recommendations 
- `pdf_generator.py` - PDF report generation
- `.streamlit/config.toml` - Streamlit configuration with dark theme

## Disclaimer

This application is for informational purposes only and should not be considered as tax advice. Always consult with a qualified tax professional for specific advice related to your tax situation.