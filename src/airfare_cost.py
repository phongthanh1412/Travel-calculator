import os
import pandas as pd
from perdiem_cost import sanitize_currency

def load_airfare_data():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, '..', 'data')
    file_path = os.path.join(data_dir, 'airfare_2025.csv')

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Airfare data file not found at {file_path}.")

    df = pd.read_csv(file_path)

    for col in ['ORIGIN_CITY_NAME', 'DESTINATION_CITY_NAME']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if 'YCA_FARE' in df.columns:
        df['YCA_FARE'] = df['YCA_FARE'].apply(sanitize_currency)

    return df

def get_airfare_origins(df):
    return ['-Select-'] + sorted(df['ORIGIN_CITY_NAME'].dropna().astype(str).unique().tolist())

def get_airfare_destinations(df, origin):
    if origin == "-Select-":
        return []
    return sorted(
        df[df['ORIGIN_CITY_NAME'] == origin]['DESTINATION_CITY_NAME']
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

def lookup_airfare(df, origin, destination):
    row = df[(df['ORIGIN_CITY_NAME'] == origin) & (df['DESTINATION_CITY_NAME'] == destination)]
    if row.empty:
        return None
    return float(row.iloc[0]['YCA_FARE'])

def generate_airfare_justification(df, origin, destination):
    display_to_df_col = {
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

    SAFE_PIPE = " ｜ "

    display_cols = list(display_to_df_col.keys())
    money_cols_df = {"YCA_FARE", "_CA_FARE"}

    rows = df[(df["ORIGIN_CITY_NAME"] == origin) & (df["DESTINATION_CITY_NAME"] == destination)]
    if rows.empty:
        return {"info_text": "**No airfare award information found for this route.**"}

    header = "| " + " | ".join(display_cols) + " |\n"
    sep = "|" + "|".join(["---"] * len(display_cols)) + "|\n"
    lines = [header, sep]

    for _, r in rows.iterrows():
        vals = []
        for disp_col in display_cols:
            df_cols = display_to_df_col[disp_col]

            if disp_col == "One-way Fare":
                yca_val = r.get("YCA_FARE", None)
                ca_val = r.get("_CA_FARE", None)
                fare_parts = []
                if pd.notna(yca_val):
                    fare_parts.append(f"YCA: ＄{float(yca_val):.0f}")
                if pd.notna(ca_val):
                    fare_parts.append(f"_CA: ＄{float(ca_val):.0f}")
                vals.append(SAFE_PIPE.join(fare_parts) if fare_parts else "")
                continue

            if isinstance(df_cols, list):
                city = str(r.get(df_cols[0], "")) if pd.notna(r.get(df_cols[0], None)) else ""
                state = r.get(df_cols[1], "")
                if pd.isna(state) or str(state).strip() == "":
                    state = r.get(df_cols[3], "")  
                state = str(state) if pd.notna(state) else ""
                airport = str(r.get(df_cols[2], "")) if pd.notna(r.get(df_cols[2], None)) else ""

                vals.append(f"{city}, {state} - {airport}" if city or state or airport else "")
            else:
                v = r.get(df_cols, "")
                if df_cols in ("EFFECTIVE_DATE", "EXPIRATION_DATE") and pd.notna(v):
                    try:
                        v = pd.to_datetime(v).strftime("%m/%d/%Y")
                    except Exception:
                        pass
                if df_cols == "AIRLINE_ABBREV":
                    v = AIRLINE_MAP.get(str(v), v)
                if df_cols == "AWARDED_SERV":
                    v = SERVICE_MAP.get(str(v), v)
                if df_cols in money_cols_df and pd.notna(v):
                    v = f"${float(v):,.0f}"
                if pd.isna(v):
                    v = ""
                vals.append(str(v))

        lines.append("| " + " | ".join(vals) + " |\n")

    info_text = "**City Pair airfares**\n" + "".join(lines)
    return {"info_text": info_text}
