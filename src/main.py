from CONSTANTS import *
import streamlit as st
from pages.home_page import home_page
from pages.perdiem_page import per_diem_page
from pages.airfare_page import airfare_page
   
def main():
    st.set_page_config(page_title="Travel Cost Estimator", layout="wide")
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Tabs", ["Home", "Per Diem", "Airfare"])

    if page == "Per Diem":
        per_diem_page()
    elif page == "Airfare":
        airfare_page()
    else:
        home_page()

if __name__ == "__main__":
    main()
