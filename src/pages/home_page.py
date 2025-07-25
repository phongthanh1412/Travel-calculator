from CONSTANTS import *
import streamlit as st

# ---------------------- HOME PAGE ----------------------
def home_page():
    st.title("Travel Cost Estimator")
    st.markdown("""
        Simplify your travel planning and keep your budget on track with our new Travel Cost Estimator, powered by the
        latest FY25 GSA per diem rates and detailed airfare information. This essential tool is perfect for anyone
        needing accurate, travel-policy-compliant cost estimates.
        No more guessing or manual calculations! Our estimator uses the FY25 General Services Administration (GSA)
        per diem rates, effective from October 1, 2024, to calculate daily allowances for hotels, meals, and small
        expenses across many U.S. (CONUS) destinations. For international or non-continental U.S. (OCONUS) trips,
        it includes updated rates from July 1, 2025.
               
        On top of daily costs, the tool uses trusted airfare data from the GSA City Pair Program to provide realistic
        flight cost estimates. Whether you're booking a single trip or managing multiple travel plans, this tool helps
        you make smart, budget-friendly decisions.
    """)