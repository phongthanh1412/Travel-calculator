from CONSTANTS import *
import streamlit as st
from pages import home, perdiem, airfare, pov

def main():
    hide_st_style = """
    <style>
    .stApp [data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    Tabs = {
        "Home": home,
        "Per Diem": perdiem,
        "Airfare": airfare,
        "POV mileage": pov
    }
    st.set_page_config(page_title="Travel Cost Estimator", layout="wide",initial_sidebar_state = 'auto')
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Tabs", list(Tabs.keys()))

    if page == "Per Diem":
        Tabs[page].per_diem_page()
    elif page == "Airfare":
        Tabs[page].airfare_page()
    elif page == "POV mileage":
        Tabs[page].pov_page()
    else:
        Tabs[page].home_page()

if __name__ == "__main__":
    main()
