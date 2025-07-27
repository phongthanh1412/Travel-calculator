import streamlit as st
import pandas as pd

def pov_page():
    st.title("POV mileage")
    st.info("GSA has adjusted all POV mileage reimbursement rates effective January 1, 2025.")
    
    st.write("**Transportation Modes and Rates**")
    data1 = {
        "Modes of transportation": [
            "Airplane",
            "If use of privately owned automobile is authorized or if no government-furnished automobile is authorized and available",
            "If government-furnished automobile is authorized and available",
            "Motorcycle"
        ],
        "Effective/applicability date": [
            "January 1, 2025",
            "January 1, 2025",
            "January 1, 2025",
            "January 1, 2025"
        ],
        "Rate per mile": ["$1.75", "$0.70", "$0.21", "$0.68"]
    }

    df1 = pd.DataFrame(data1)
    st.dataframe(df1)

    st.write("**Standard Relocation Rate**")
    data2 = {
        "Relocation": "Standard mileage rate for moving purposes",
        "Effective/applicability date": "January 1, 2025",
        "Rate per mile": "$0.21"
    }

    df2 = pd.DataFrame(data2, index=[0])  
    st.dataframe(df2)