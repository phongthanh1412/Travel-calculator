import os
import pandas as pd
from datetime import datetime

def load_travel_data():
    """Load per diem data from the updated FY2025 CSV file."""
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, '..', 'data')
    file_path = os.path.join(data_dir, 'FY2025_PerDiemRates.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}. Please check the path or file name.")
    
    df = pd.read_csv(file_path)
    df = df[df['ID'].notna()]  
    
    current_year = datetime.now().year
    df['Season Begin'] = df['SEASON BEGIN'].apply(lambda x: parse_date(x, current_year) if pd.notna(x) else pd.NaT)
    df['Season End'] = df['SEASON END'].apply(lambda x: parse_date(x, current_year) if pd.notna(x) else pd.NaT)
    df['Normalized_Destination'] = df.apply(lambda row: f"{row['DESTINATION'].lower().strip()}_{row['STATE'].lower().strip()}", axis=1)
    
    return df

def parse_date(date_str, year):
    if pd.isna(date_str) or not isinstance(date_str, str):
        return pd.NaT
    try:
        return pd.to_datetime(f"{date_str.strip()} {year}", format='%B %d %Y')
    except ValueError:
        return pd.NaT

def fetch_state_cities(df, state):
    filtered = df[df['STATE'].str.lower() == state.lower()]
    return sorted(filtered['DESTINATION'].unique().tolist())

def get_states_list(df):
    states = df['STATE'].fillna('Unknown').astype(str).unique()
    return ['-Select-'] + sorted(states)

def convert_state_abbr_to_full(abbr):
    state_map = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia",
        "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
        "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
        "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
        "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
        "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
        "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
        "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
        "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia",
        "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
    }
    return state_map.get(abbr.upper(), abbr)

def get_travel_rates(city, state, start_date, end_date, df):
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    norm_city = f"{city.lower().strip()}_{state.lower().strip()}"
    
    filtered_data = df[df['Normalized_Destination'] == norm_city]
    for _, row in filtered_data.iterrows():
        start = row['Season Begin']
        end = row['Season End']
        
        start_date_obj = start.to_pydatetime().date() if pd.notna(start) else None
        end_date_obj = end.to_pydatetime().date() if pd.notna(end) else None
        
        if start_date_obj is None and end_date_obj is None:
            return row['FY25 Lodging Rate'], row['FY25 M&IE']
        
        if (start_date_obj and end_date_obj and 
            start_date_obj <= start_dt.date() <= end_date_obj and 
            start_date_obj <= end_dt.date() <= end_date_obj):
            return row['FY25 Lodging Rate'], row['FY25 M&IE']
    
    return None, None

def sanitize_currency(value):
    if pd.isna(value) or value is None:
        return 0.0
    if isinstance(value, str):
        value = value.replace('$', '').replace(',', '')
    try:
        return float(value)
    except ValueError:
        return 0.0

def compute_travel_expenses(start_date, end_date, airfare_cost, lodging_cost, mie_cost):
    airfare_cost = sanitize_currency(airfare_cost)
    lodging_cost = sanitize_currency(lodging_cost)
    mie_cost = sanitize_currency(mie_cost)
    
    days_count = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1
    nights_count = days_count - 1
    airfare_total = airfare_cost * 2
    lodging_total = nights_count * lodging_cost
    first_last_mie = mie_cost * 0.75 * 2
    middle_mie = mie_cost * (days_count - 2)
    mie_total = first_last_mie + middle_mie
    
    perdiem_total = lodging_total + mie_total
    return {
        "Airfare RT": int(airfare_total),
        "Lodging Rate": format(int(lodging_cost)),
        "Max lodging total": format(int(lodging_total)),
        "Total Days": days_count,
        "Hotel Nights": nights_count,
        "MIE Rate": mie_cost,
        "First/Last MIE": f"{first_last_mie:.2f}",
        "Middle Days MIE": f"{int(middle_mie)}",
        "M&IE total": f"{int(mie_total)}",
        "Estimated per diem total": f"{int(perdiem_total)}",
    }

def generate_budget_justification(state, city, start_date, end_date, costs):
    lodging_text = (
        f"**Lodging Breakdown**\n"
        f"| Date | Daily Rate | Nights | Total |\n"
        f"|---|---|---|---|\n"
        f"| {pd.to_datetime(start_date).strftime('%B')} | ${costs['Lodging Rate']} | {costs['Hotel Nights']} | ${costs['Max lodging total']} |"
    )
    
    mie_text = (
        f"**Meals & Incidental Expenses Breakdown**\n"
        f"| Days, Month | Daily Rate | Days | Total |\n"
        f"|---|---|---|---|\n"
        f"| First day ({pd.to_datetime(start_date).strftime('%m/%d/%Y')}) | ${float(costs['First/Last MIE'])/2:.2f} | 1 | ${float(costs['First/Last MIE'])/2:.2f} |\n"
        f"| Full day ({pd.to_datetime(start_date).strftime('%B')}) | ${costs['MIE Rate']} | {costs['Total Days'] - 2} | ${costs['Middle Days MIE']} |\n"
        f"| Last day ({pd.to_datetime(end_date).strftime('%m/%d/%Y')}) | ${float(costs['First/Last MIE'])/2:.2f} | 1 | ${float(costs['First/Last MIE'])/2:.2f} |\n"
    )
    return {"lodging_text": lodging_text, "mie_text": mie_text}
