SELECT = "-Select-"
SAFE_PIPE = " ｜ "

STATE_MAP = {
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

HEADER_MAP = {
    "Origin": ["ORIGIN_CITY_NAME", "ORIGIN_STATE", "ORIGIN_AIRPORT_ABBREV", "ORIGIN_COUNTRY"],
    "Destination": ["DESTINATION_CITY_NAME", "DESTINATION_STATE", "DESTINATION_AIRPORT_ABBREV", "DESTINATION_COUNTRY"],
    "Airline": "AIRLINE_ABBREV",
    "Service": "AWARDED_SERV",
    "One-way Fare": ["YCA_FARE", "_CA_FARE"],
    "Effective Date": "EFFECTIVE_DATE",
    "Expiration Date": "EXPIRATION_DATE",
}

AIRLINE_MAP = {
    "3M": "Silver Airways",
    "AA": "American Airlines",
    "AS": "Alaska Airlines",
    "B6": "JetBlue",
    "DL": "Delta",
    "HA": "Hawaiian Airlines",
    "MX": "Mexicana de Aviación (no longer)",
    "UA": "United Airlines",
    "WN": "Southwest Airlines",
}

SERVICE_MAP = {
    "C": "Connect",
    "N": "Non-stop"
}