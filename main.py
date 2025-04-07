"""
TaxBot India - Income Tax Calculator and Advisor
A Streamlit-based application that helps Indian taxpayers 
compare tax regimes and save on taxes.
"""

import streamlit as st
import io
from datetime import date
from tax_calculator import (
    calculate_old_regime_tax,
    calculate_new_regime_tax,
    get_tax_saving_tips,
    get_better_regime
)
from pdf_generator import generate_tax_report

# Page configuration
st.set_page_config(
    page_title="TaxBot India",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="🧾"
)

# App title and description
st.title("🧾 TaxBot India")
st.subheader("Save Smarter, Grow Faster")

st.markdown("""
This tool helps you calculate your income tax under both the old and new tax regimes, 
compare them, and get personalized tax-saving recommendations.
""")

# Create two columns for the form
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Income Details")
    income = st.number_input("💰 Annual Income (in ₹)", min_value=0, value=0, step=10000, format="%d")
    investments = st.number_input("📦 80C Investments (in ₹)", min_value=0, value=0, step=5000, format="%d", 
                              help="PPF, ELSS, NSC, Tax Saving FD, LIC, etc. (Max: ₹1,50,000)")
    health_insurance = st.number_input("🏥 Health Insurance Premium (₹)", min_value=0, value=0, step=1000, format="%d",
                                  help="Section 80D (Max: ₹25,000 for self & family)")

with col2:
    st.markdown("### Deductions")
    home_loan = st.number_input("🏠 Home Loan Interest (₹)", min_value=0, value=0, step=10000, format="%d",
                            help="Section 24b (Max: ₹2,00,000)")
    edu_loan = st.number_input("🎓 Education Loan Interest (₹)", min_value=0, value=0, step=5000, format="%d",
                           help="Section 80E (No upper limit)")
    hra = st.number_input("🏙️ HRA Exemption (₹)", min_value=0, value=0, step=10000, format="%d",
                       help="House Rent Allowance Exemption")

# Calculate button
if st.button("📊 Calculate Tax", type="primary"):
    # Calculate total deductions
    total_deductions = investments + health_insurance + home_loan + edu_loan + hra
    
    # Calculate taxable income under both regimes
    old_regime_taxable = max(0, income - total_deductions)
    new_regime_taxable = income  # No deductions in new regime
    
    # Calculate taxes
    old_regime_tax = calculate_old_regime_tax(old_regime_taxable)
    new_regime_tax = calculate_new_regime_tax(income)
    
    # Determine better regime
    better_regime = get_better_regime(old_regime_tax, new_regime_tax)
    
    # Get tax saving tips
    tips = get_tax_saving_tips(income, investments, health_insurance, home_loan, edu_loan)
    
    # Display results
    st.markdown("---")
    st.markdown("### 🔍 Tax Regime Comparison")
    
    # Create two columns for tax comparison
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("**Old Tax Regime**")
        st.markdown(f"Taxable Income: ₹{old_regime_taxable:,}")
        st.markdown(f"Base Tax: ₹{old_regime_tax['base_tax']:,.2f}")
        st.markdown(f"Cess (4%): ₹{old_regime_tax['cess']:,.2f}")
        st.markdown(f"**Total Tax: ₹{old_regime_tax['total_tax']:,.2f}**")
    
    with right_col:
        st.markdown("**New Tax Regime**")
        st.markdown(f"Taxable Income: ₹{new_regime_taxable:,}")
        st.markdown(f"Base Tax: ₹{new_regime_tax['base_tax']:,.2f}")
        st.markdown(f"Cess (4%): ₹{new_regime_tax['cess']:,.2f}")
        st.markdown(f"**Total Tax: ₹{new_regime_tax['total_tax']:,.2f}**")
    
    # Recommendation box
    st.markdown("---")
    st.markdown("### 🎯 Recommendation")
    
    if better_regime["regime"] == "Old Regime":
        color = "green"
    else:
        color = "blue"
    
    st.markdown(f"""
    <div style='background-color:{color}33; padding:10px; border-radius:5px;'>
        <h4 style='color:{color};'>💡 {better_regime["regime"]} is better for you!</h4>
        <p>You will save approximately <b>₹{better_regime["savings"]:,.2f}</b> by choosing this regime.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tax saving tips
    st.markdown("---")
    st.markdown("### ✅ Tax Saving Tips")
    
    for tip in tips:
        st.markdown(f"🟢 {tip}")
    
    # Prepare data for PDF generator
    user_data = {
        "income": income,
        "investments": investments,
        "health_insurance": health_insurance,
        "home_loan": home_loan,
        "edu_loan": edu_loan,
        "total_deductions": total_deductions,
        "old_regime_taxable": old_regime_taxable
    }
    
    # Generate PDF
    pdf_bytes = generate_tax_report(user_data, old_regime_tax, new_regime_tax, better_regime, tips)
    
    # Provide download button for PDF
    st.download_button(
        label="📄 Download Tax Report PDF",
        data=pdf_bytes,
        file_name=f"TaxBot_Report_{date.today().strftime('%d-%m-%Y')}.pdf",
        mime="application/pdf"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <p style='font-size: small;'>
        <b>TaxBot India</b> • Calculate, Compare, Save<br>
        <i>This tool is for informational purposes only. Always consult a tax professional for specific advice.</i>
    </p>
</div>
""", unsafe_allow_html=True)
