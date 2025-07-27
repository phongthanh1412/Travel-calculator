from CONSTANTS import *
import streamlit as st
from perdiem_cost import (
    load_travel_data, get_states_list, fetch_state_cities,
    get_travel_rates, compute_travel_expenses,
    generate_budget_justification, convert_state_abbr_to_full 
)

# ---------------------- PER DIEM PAGE ----------------------
def per_diem_page():
    st.title("Per Diem Look-up")

    if st.session_state.get("_reset_perdiem", False):
        for k in [
            "pd_state", "pd_city", "pd_start", "pd_end", "pd_travelers",
            "pd_cost_breakdown", "pd_justification",
            "pd_search_btn", "pd_reset_btn"
        ]:
            st.session_state.pop(k, None)
        st.session_state["_reset_perdiem"] = False  

    try:
        travel_df = load_travel_data()
        state_options = get_states_list(travel_df)
    except FileNotFoundError as e:
        st.error(str(e))
        return

    left_section, right_section = st.columns(2)
    with left_section:
        st.write("**Choose a location**")
        state_value = st.session_state.get("pd_state", SELECT)
        if state_value not in state_options:
            state_value = SELECT
        selected_state = st.selectbox("State", state_options, index=state_options.index(state_value), key="pd_state")

        city_list = fetch_state_cities(travel_df, selected_state)
        selected_city = st.selectbox("City", city_list, key="pd_city")
        if selected_state == SELECT:
            st.warning("Please select a state and city.")

    with right_section:
        st.write("**Choose a date**")
        if selected_state == SELECT:
            st.date_input("Travel start date (mm/dd/yyyy)", value=None, disabled=True)
            st.date_input("Travel end date (mm/dd/yyyy)", value=None, disabled=True)
            st.warning("Please select a state first to choose dates.")
        else:
            travel_start = st.date_input("Travel start date (mm/dd/yyyy)")
            travel_end = st.date_input("Travel end date (mm/dd/yyyy)")

    col_1, col_2, _, _ = st.columns([1, 1, 1, 1])
    with col_1:
        search_clicked = st.button("Search", use_container_width=True, key="pd_search_btn")
    with col_2:
        reset_clicked = st.button("Reset", use_container_width=True, key="pd_reset_btn")

    if reset_clicked:
        st.session_state["_reset_perdiem"] = True
        st.rerun()

    if search_clicked:
        if travel_end < travel_start:
            st.error("End date must be after start date.")
            st.stop()

        lodging_rate, mie_rate = get_travel_rates(selected_city, selected_state, travel_start, travel_end, travel_df)
        if lodging_rate is None or mie_rate is None:
            st.error("No available rates for the selected city and dates. Please try another option.")
            st.stop()

        cost_breakdown = compute_travel_expenses(
            travel_start, travel_end, 0.0, lodging_rate, mie_rate
        )

        state_full = convert_state_abbr_to_full(selected_state)
        st.subheader(f"Your search for {selected_city}, {state_full}")

        st.markdown(
            f"""
            <h3 style='margin-bottom: 0;'>Estimated per diem total: ${cost_breakdown['Estimated per diem total']}</h3>
            <span style='color: black; font-size: 16px;'>Estimated per diem total = Max lodging total + M&IE total</span>
            """,
            unsafe_allow_html=True
        )

        justification = generate_budget_justification(
            selected_state, selected_city, travel_start, travel_end, cost_breakdown
        )

        left_col, right_col = st.columns(2)
        with right_col:
            st.write(justification["lodging_text"])
            st.success(f"**Max lodging total: ${int(cost_breakdown['Max lodging total'])}**")

        with left_col:
            st.write(justification["mie_text"])
            st.info("*The first and last calendar dates of M&IE are calculated at 75%.*")
            mie_total = float(cost_breakdown['First/Last MIE']) + float(cost_breakdown['Middle Days MIE'])
            st.success(f"**M&IE total: ${mie_total:.0f}**")
