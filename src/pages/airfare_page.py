from CONSTANTS import *
import streamlit as st
from airfare_cost import (load_airfare_data, get_airfare_origins,
    get_airfare_destinations, lookup_airfare, generate_airfare_justification)

# ---------------------- AIRFARE PAGE ----------------------
def airfare_page():
    st.title("Airfare Look-up")

    if st.session_state.get("_reset_airfare", False):
        for k in ["af_origin", "af_destination", "af_search_btn", "af_reset_btn"]:
            st.session_state.pop(k, None)
        st.session_state["_reset_airfare"] = False 

    try:
        airfare_df = load_airfare_data()
        origin_options = get_airfare_origins(airfare_df)  
    except FileNotFoundError as e:
        st.error(str(e))
        return

    col_a, col_b = st.columns(2)
    with col_a:
        origin_value = st.session_state.get("af_origin", SELECT)
        if origin_value not in origin_options:
            origin_value = SELECT
        try:
            origin_index = origin_options.index(origin_value)
        except ValueError:
            origin_index = 0

        selected_origin = st.selectbox(
            "Origin city or airport",
            origin_options,
            index=origin_index,
            key="af_origin"
        )

    with col_b:
        if selected_origin == SELECT:
            st.selectbox(
                "Destination city or airport",
                [SELECT],
                index=0,
                key="af_destination",
                disabled=True
            )
        else:
            dest_options = [SELECT] + get_airfare_destinations(airfare_df, selected_origin)
            dest_value = st.session_state.get("af_destination", SELECT)
            if dest_value not in dest_options:
                dest_value = SELECT
            try:
                dest_index = dest_options.index(dest_value)
            except ValueError:
                dest_index = 0

            st.selectbox(
                "Destination city or airport",
                dest_options,
                index=dest_index,
                key="af_destination"
            )
    st.info(
        "All fares are listed one-way and are valid in either direction. "
    )

    with st.expander("**More details about airfares**", expanded=False):
        st.markdown("""
            **Taxes and fees may apply to the final price.**  
            The final ticket price, excluding baggage fees, will be displayed in your agency’s approved travel 
            management system. Information on commercial baggage fees is available on the
            [Airline Information](https://www.gsa.gov/node/82478) page.  
                    
            **Domestic**    
            Domestic fares already include all applicable Federal, State, and local taxes, as well as airport 
            maintenance and administrative fees. However, they do not cover additional charges such as
            passenger facility charges, segment fees, or passenger security service fees.  

            **International**    
            International fares exclude taxes and other fees but include fuel surcharges.
            """)

    c1, c2, _, _ = st.columns([1, 1, 1, 1])
    with c1:
        search_clicked = st.button("Search", use_container_width=True, key="af_search_btn")
    with c2:
        reset_clicked = st.button("Reset", use_container_width=True, key="af_reset_btn")

    if reset_clicked:
        st.session_state["_reset_airfare"] = True
        st.rerun()

    if search_clicked:
        if selected_origin == SELECT:
            st.error("Please select a valid origin.")
            return

        selected_destination = st.session_state.get("af_destination", SELECT)
        if selected_destination in (SELECT, "", None):
            st.error("Please select a valid destination.")
            return

        fare = lookup_airfare(airfare_df, selected_origin, selected_destination)
        if fare is None or fare <= 0:
            st.error("No airfare found for this route.")
            return

        justi = generate_airfare_justification(airfare_df, selected_origin, selected_destination)
        st.markdown(justi["info_text"])
