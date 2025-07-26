import os
import pandas as pd
from CONSTANTS import *

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

    return df

def get_airfare_origins(df):
    return [SELECT] + sorted(df['ORIGIN_CITY_NAME'].dropna().astype(str).unique().tolist())

def get_airfare_destinations(df, origin):
    if origin == SELECT:
        return []
    return [SELECT] + sorted(
        df[df['ORIGIN_CITY_NAME'] == origin]['DESTINATION_CITY_NAME'].dropna().astype(str).unique().tolist()
    )

def lookup_airfare(df, origin, destination):
    row = df[(df['ORIGIN_CITY_NAME'] == origin) & (df['DESTINATION_CITY_NAME'] == destination)]
    if row.empty:
        return None
    return float(row.iloc[0]['YCA_FARE'])

def generate_airfare_justification(df, origin, destination):
    
    display_cols = list(HEADER_MAP.keys())
    money_cols_df = {"YCA_FARE", "_CA_FARE"}

    rows = df[(df["ORIGIN_CITY_NAME"] == origin) & (df["DESTINATION_CITY_NAME"] == destination)]
    if rows.empty:
        return {"info_text": "**No airfare award information found for this route.**"}

    header = "| " + " | ".join(display_cols) + " |\n"
    sep = "|" + "|".join(["---"] * len(display_cols)) + "|\n"
    lines = [header, sep]

    for _, row in rows.iterrows():
        vals = []
        for disp_col in display_cols:
            df_cols = HEADER_MAP[disp_col]

            if disp_col == "One-way Fare":
                yca_val = row.get("YCA_FARE", None)
                ca_val = row.get("_CA_FARE", None)
                fare_parts = []
                if pd.notna(yca_val):
                    fare_parts.append(f"YCA: ＄{float(yca_val):.0f}")
                if pd.notna(ca_val):
                    fare_parts.append(f"_CA: ＄{float(ca_val):.0f}")
                vals.append(SAFE_PIPE.join(fare_parts) if fare_parts else "")
                continue

            if isinstance(df_cols, list):
                city = str(row.get(df_cols[0], "")) if pd.notna(row.get(df_cols[0], None)) else ""
                state = row.get(df_cols[1], "")
                if pd.isna(state) or str(state).strip() == "":
                    state = row.get(df_cols[3], "")  
                state = str(state) if pd.notna(state) else ""
                airport = str(row.get(df_cols[2], "")) if pd.notna(row.get(df_cols[2], None)) else ""

                vals.append(f"{city}, {state} - {airport}" if city or state or airport else "")
            
            else:
                val = row.get(df_cols, "")
                if df_cols in ("EFFECTIVE_DATE", "EXPIRATION_DATE") and pd.notna(val):
                    try:
                        val = pd.to_datetime(val).strftime("%m/%d/%Y")
                    except Exception:
                        pass
                if df_cols == "AIRLINE_ABBREV":
                    val = AIRLINE_MAP.get(str(val), val)
                if df_cols == "AWARDED_SERV":
                    val = SERVICE_MAP.get(str(val), val)
                if df_cols in money_cols_df and pd.notna(val):
                    val = f"${float(val):.0f}"
                if pd.isna(val):
                    val = ""
                vals.append(str(val))

        lines.append("| " + " | ".join(vals) + " |\n")

    info_text = "**City Pair Airfares**\n" + "".join(lines)
    return {"info_text": info_text}