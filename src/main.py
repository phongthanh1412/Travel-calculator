import streamlit as st
from perdiem_cost import (
    load_travel_data, get_states_list, fetch_state_cities,
    get_travel_rates, compute_travel_expenses,
    generate_budget_justification, convert_state_abbr_to_full,
    
)
from airfare_cost import (load_airfare_data, get_airfare_origins,
    load_airfare_data, get_airfare_origins, get_airfare_destinations, lookup_airfare)
    
st.set_page_config(page_title="Travel Cost Estimator", layout="wide")

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
# ---------------------- PER DIEM PAGE ----------------------
def per_diem_page():
    st.title("Per Diem Look-up")

    try:
        travel_df = load_travel_data()
        state_options = get_states_list(travel_df)
    except FileNotFoundError as e:
        st.error(str(e))
        return

    left_section, right_section = st.columns(2)
    with left_section:
        st.write("**Choose a location**")
        selected_state = st.selectbox("State", state_options, index=0, key="pd_state")
        city_list = fetch_state_cities(travel_df, selected_state)
        selected_city = st.selectbox("City", city_list, key="pd_city")
        if selected_state == "-Select-":
            st.warning("Please select a state and city.")

    with right_section:
        st.write("**Choose a date**")
        if selected_state == "-Select-":
                st.date_input("Travel start date (mm/dd/yyyy)", value=None, disabled=True)
                st.date_input("Travel end date (mm/dd/yyyy)", value=None, disabled=True)
                st.warning("Please select a state first to choose dates.")
        else:
                travel_start = st.date_input("Travel start date (mm/dd/yyyy)")
                travel_end = st.date_input("Travel end date (mm/dd/yyyy)")
                # traveler_count = st.number_input("Number of Travelers", min_value=1, step=1)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        search_clicked = st.button("Search", use_container_width=True)
    with col2:
        reset_clicked = st.button("Reset", use_container_width=True)

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
            st.write(f"**Max lodging total: ${int(cost_breakdown['Max lodging total'])}**")

        with left_col:
            st.write(justification["mie_text"])
            st.write("*The first and last calendar dates of M&IE are calculated at 75%.*")
            mie_total = float(cost_breakdown['First/Last MIE']) + float(cost_breakdown['Middle Days MIE'])
            st.write(f"**M&IE total: ${mie_total:.0f}**")

    if reset_clicked:
        for k in [
            "pd_state", "pd_city", "pd_start", "pd_end", "pd_travelers",
            "pd_cost_breakdown", "pd_justification"
        ]:
            st.session_state.pop(k, None)
        st.rerun()


# ---------------------- AIRFARE PAGE ----------------------
def airfare_page():
    st.title("Airfare Look-up")

    try:
        airfare_df = load_airfare_data()
        origin_options = get_airfare_origins(airfare_df)
    except FileNotFoundError as e:
        st.error(str(e))
        return

    col_a, col_b = st.columns(2)
    with col_a:
        selected_origin = st.selectbox(
            "Origin city or airport",
            origin_options if origin_options else ["-Select-"],
            index=0,
            key="af_origin"
        )
    with col_b:
        dest_options = get_airfare_destinations(airfare_df, selected_origin) if selected_origin != "-Select-" else []
        selected_destination = st.selectbox(
            "Destination city or airport",
            dest_options if dest_options else ["-Select-"],
            key="af_destination"
        )

    c1, c2, _, _ = st.columns([1, 1, 2, 2])
    with c1:
        search_clicked = st.button("Search", use_container_width=True, key="af_search_btn")
    with c2:
        reset_clicked = st.button("Reset", use_container_width=True, key="af_reset_btn")

    if reset_clicked:
        for k in ["af_origin", "af_destination", "af_search_btn"]:
            st.session_state.pop(k, None)
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

    if search_clicked:
        if selected_origin == "-Select-" or selected_destination in ("", "-Select-"):
            st.error("Please select a valid origin and destination.")
            return

        fare = lookup_airfare(airfare_df, selected_origin, selected_destination)
        if fare is None or fare <= 0:
            st.error("No airfare found for this route.")
            return

        st.success(
            f"""
            **One-way Airfare:** ${fare:.0f}\n  
            **Round-trip Airfare (x2):** ${fare * 2:.0f}
            """
        )

# ---------------------- MAIN ----------------------
def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Go to", ["Home", "Per Diem", "Airfare"])

    if page == "Per Diem":
        per_diem_page()
    elif page == "Airfare":
        airfare_page()
    else:
        home_page()

if __name__ == "__main__":
    main()
