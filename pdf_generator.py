"""
PDF Generator Module for TaxBot India
Generates detailed tax reports as downloadable PDFs
"""

from fpdf import FPDF
import datetime

class TaxReportPDF(FPDF):
    """Custom PDF class for generating tax reports"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """Define the header of each page"""
        # Set font
        self.set_font("Arial", "B", 15)
        # Title
        self.cell(0, 10, "TaxBot India - Tax Report", 0, 1, "C")
        # Date
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, f"Generated on: {datetime.datetime.now().strftime('%d %b %Y, %H:%M')}", 0, 1, "C")
        # Line break
        self.ln(5)
    
    def footer(self):
        """Define the footer of each page"""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    
    def chapter_title(self, title):
        """Add a chapter title"""
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, "L", True)
        self.ln(4)
    
    def chapter_body(self, body):
        """Add chapter content"""
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 5, body)
        self.ln()
    
    def add_table_header(self, headers):
        """Add table header row"""
        self.set_font("Arial", "B", 11)
        self.set_fill_color(232, 232, 232)
        for header in headers:
            self.cell(40, 7, header, 1, 0, "C", True)
        self.ln()
    
    def add_table_row(self, data):
        """Add table data row"""
        self.set_font("Arial", "", 10)
        for item in data:
            self.cell(40, 6, str(item), 1, 0, "C")
        self.ln()

def generate_tax_report(user_data, old_regime, new_regime, better_regime, tips):
    """
    Generate PDF tax report
    
    Args:
        user_data: Dictionary with user input data
        old_regime: Tax calculation for old regime
        new_regime: Tax calculation for new regime
        better_regime: Information about the better regime
        tips: List of tax saving tips
        
    Returns:
        PDF file bytes
    """
    pdf = TaxReportPDF()
    
    # Add first page
    pdf.add_page()
    
    # User Details
    pdf.chapter_title("Your Income Details")
    income_details = (
        f"Annual Income: Rs. {user_data['income']:,}\n"
        f"Section 80C Investments: Rs. {user_data['investments']:,}\n"
        f"Health Insurance Premium: Rs. {user_data['health_insurance']:,}\n"
        f"Home Loan Interest: Rs. {user_data['home_loan']:,}\n"
        f"Education Loan Interest: Rs. {user_data['edu_loan']:,}\n"
        f"Total Deductions: Rs. {user_data['total_deductions']:,}"
    )
    pdf.chapter_body(income_details)
    
    # Tax Calculation Section
    pdf.chapter_title("Tax Calculation")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, f"Old Regime Taxable Income: Rs. {user_data['old_regime_taxable']:,}", 0, 1)
    pdf.cell(0, 6, f"New Regime Taxable Income: Rs. {user_data['income']:,}", 0, 1)
    pdf.ln(5)
    
    # Tax Comparison Table
    pdf.chapter_title("Tax Regime Comparison")
    pdf.add_table_header(["Details", "Old Regime", "New Regime"])
    
    # Format currency values - use "Rs." instead of ₹ symbol for encoding compatibility
    old_base_tax = f"Rs. {old_regime['base_tax']:,.2f}"
    old_cess = f"Rs. {old_regime['cess']:,.2f}"
    old_total = f"Rs. {old_regime['total_tax']:,.2f}"
    
    new_base_tax = f"Rs. {new_regime['base_tax']:,.2f}"
    new_cess = f"Rs. {new_regime['cess']:,.2f}"
    new_total = f"Rs. {new_regime['total_tax']:,.2f}"
    
    # Add table rows
    pdf.add_table_row(["Base Tax", old_base_tax, new_base_tax])
    pdf.add_table_row(["Cess (4%)", old_cess, new_cess])
    pdf.add_table_row(["Total Tax", old_total, new_total])
    
    # Better Regime Section
    pdf.ln(5)
    pdf.chapter_title("Recommended Tax Regime")
    better_regime_text = (
        f"Based on your inputs, the {better_regime['regime']} is better for you.\n"
        f"You will save approximately Rs. {better_regime['savings']:,.2f} by choosing this regime."
    )
    pdf.chapter_body(better_regime_text)
    
    # Tax Saving Tips
    pdf.add_page()
    pdf.chapter_title("Tax Saving Recommendations")
    
    for i, tip in enumerate(tips, 1):
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{i}. {tip}", 0, 1)
    
    # Disclaimer
    pdf.ln(10)
    pdf.set_font("Arial", "I", 9)
    disclaimer = (
        "Disclaimer: This report is for informational purposes only and should not be considered as tax advice. "
        "Tax laws are subject to change. Please consult with a qualified tax professional for specific advice "
        "related to your tax situation."
    )
    pdf.multi_cell(0, 5, disclaimer)
    
    # Get the PDF content as bytes
    pdf_bytes = pdf.output(dest="S")
    # Return the bytes directly as they're already encoded
    return pdf_bytes
