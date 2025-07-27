from CONSTANTS import *
import streamlit as st

# ---------------------- HOME PAGE ----------------------
def home_page():
    st.title("Travel Cost Estimator")
    st.markdown("""
        Simplify your travel planning and keep your budget on track with Travel Cost Estimator, powered by the
        latest FY25 GSA per diem rates and detailed airfare information. This essential tool is perfect for anyone
        needing accurate, travel-policy-compliant cost estimates.
                
        No more guessing or manual calculations! This estimator uses the FY25 General Services Administration (GSA)
        per diem rates, effective from October 1, 2024, to calculate daily allowances for hotels, meals, and small
        expenses across many U.S. (CONUS) destinations. For international or non-continental U.S. (OCONUS) trips,
        it includes updated rates from July 1, 2025.
               
        On top of daily costs, the tool uses trusted airfare data from the GSA City Pair Program to provide realistic
        flight cost estimates. Whether you're booking a single trip or managing multiple travel plans, this tool helps
        you make smart, budget-friendly decisions.     
        
        ## **Per Diem**
        Per diem is a daily allowance provided to employees or travelers to cover expenses incurred while traveling for work.
        It typically includes costs for lodging, meals, and incidental expenses. The per diem rates are set by the GSA and are
                 updated annually to reflect changes in the cost of living in various locations.
                
        ### **Lodging Per Diem**
        The lodging per diem specifically pertains to accommodation expenses. This component of per diem is established by 
        the U.S. General Services Administration (GSA) and can vary considerably depending on the geographical location of 
                the travel.

        *Lodging Per Diem Calculation*:
        The lodging per diem is determined based on the average market rates of standard commercial hotels within the area. 
        It is intended to provide a reasonable reimbursement allowance that covers the cost of a standard room, inclusive of 
        applicable taxes and mandatory fees.

        *Key Factors in Lodging Allowance*:
        When setting lodging allowances, the GSA evaluates factors such as seasonal rate fluctuations, local events or peak 
        travel periods, and overall market demand to ensure the per diem rate remains equitable, adequate, and aligned with 
                prevailing accommodation costs.

        ### **Meals and Incidental Expenses (M&IE)**
    
        On the departure day from the Permanent Duty Station (PDS) and on the return day, the traveler is entitled to 75%
                 of the applicable Meals and Incidental Expenses (M&IE) rate, regardless of the actual time of departure or arrival. No exceptions or waivers to this policy are authorized.
        For the departure day, the applicable M&IE rate is determined by the Temporary Duty (TDY) location. For the return 
                day, the applicable M&IE rate is based on the final TDY location prior to returning to the PDS.

        The 75% rule also applies on the day of departure from a previous PDS and on the day of arrival at a new PDS, under 
                certain conditions, depending on the traveler's status as either a civilian employee or a Service member. 
                
        
        The Government Meal Rate (GMR) or Proportional Meal Rate (PMR) is not applicable on the first and last days of official travel.
                
        ### **Privately owned vehicle (POV) mileage reimbursement rates**
                
                Privately Owned Vehicle (POV) mileage reimbursement rates are payments per mile to cover costs like fuel, maintenance, 
                insurance, and depreciation for using personal vehicles for official business travel, typically for federal employees or
                 contractors. The U.S. General Services Administration (GSA) establishes these rates, often aligning with the IRS business
                 mileage rates, with separate calculations for airplanes and motorcycles.
                
    """)