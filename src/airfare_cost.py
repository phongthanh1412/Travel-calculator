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
        "Origin": ["ORIGIN_CITY_NAME", "ORIGIN_STATE", "ORIGIN_AIRPORT_ABBREV"],
        "Destination": ["DESTINATION_CITY_NAME", "DESTINATION_STATE", "DESTINATION_AIRPORT_ABBREV"],
        "Airline": "AIRLINE_ABBREV",
        "Service": "AWARDED_SERV",
        "One-way Fare": ["YCA_FARE", "_CA_FARE"],
        "Effective Date": "EFFECTIVE_DATE",
        "Expiration Date": "EXPIRATION_DATE",
    }

    def md_escape(val: str) -> str:
        return str(val).replace("|", r"\|")

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
                fare_str = []
                if pd.notna(yca_val):
                    try:
                        fare_str.append(f"YCA: $ {float(yca_val):,.0f}")
                    except Exception:
                        fare_str.append("YCA: N/A")
                if pd.notna(ca_val):
                    try:
                        fare_str.append(f"_CA: $ {float(ca_val):,.0f}")
                    except Exception:
                        fare_str.append("_CA: N/A")
                # Join with a single space and pipe, then escape the entire string
                vals.append(md_escape("-".join(fare_str) if fare_str else ""))
                continue

            if isinstance(df_cols, list):
                city = str(r.get(df_cols[0], "")) if pd.notna(r.get(df_cols[0], None)) else ""
                state = str(r.get(df_cols[1], "")) if pd.notna(r.get(df_cols[1], None)) else ""
                airport = str(r.get(df_cols[2], "")) if pd.notna(r.get(df_cols[2], None)) else ""
                vals.append(f"({city}, {state}-{airport})" if city or state or airport else "")
            else:
                v = r.get(df_cols, "")
                if df_cols in money_cols_df and pd.notna(v):
                    try:
                        v = f"${float(v):,.0f}"
                    except Exception:
                        pass
                if pd.isna(v):
                    v = ""
                vals.append(str(v))

        escaped_vals = [md_escape(v) for v in vals]
        lines.append("| " + " | ".join(escaped_vals) + " |\n")

    info_text = "**Award information**\n" + "".join(lines)
    return {"info_text": info_text}
    display_to_df_col = {
        "Origin": ["ORIGIN_CITY_NAME", "ORIGIN_STATE", "ORIGIN_AIRPORT_ABBREV"],
        "Destination": ["DESTINATION_CITY_NAME", "DESTINATION_STATE", "DESTINATION_AIRPORT_ABBREV"],
        "Airline": "AIRLINE_ABBREV",
        "Service": "AWARDED_SERV",
        "One-way Fare": ["YCA_FARE", "_CA_FARE"],
        "Effective Date": "EFFECTIVE_DATE",
        "Expiration Date": "EXPIRATION_DATE",
    }

    def md_escape(val: str) -> str:
        return str(val).replace("|", r"\|")

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
                parts = []
                if pd.notna(yca_val):
                    try:
                        parts.append(f"YCA: ${float(yca_val):,.0f}")
                    except Exception:
                        parts.append("YCA: N/A")
                if pd.notna(ca_val):
                    try:
                        parts.append(f"_CA: ${float(ca_val):,.0f}")
                    except Exception:
                        parts.append("_CA: N/A")
                # Join parts without escaping the separator
                fare_str = " | ".join(md_escape(p) for p in parts) if parts else ""
                vals.append(fare_str)
                continue

            if isinstance(df_cols, list):
                city = str(r.get(df_cols[0], "")) if pd.notna(r.get(df_cols[0], None)) else ""
                state = str(r.get(df_cols[1], "")) if pd.notna(r.get(df_cols[1], None)) else ""
                airport = str(r.get(df_cols[2], "")) if pd.notna(r.get(df_cols[2], None)) else ""
                vals.append(f"({city}, {state}-{airport})" if city or state or airport else "")
            else:
                v = r.get(df_cols, "")
                if df_cols in money_cols_df and pd.notna(v):
                    try:
                        v = f"${float(v):,.0f}"
                    except Exception:
                        pass
                if pd.isna(v):
                    v = ""
                vals.append(str(v))

        escaped_vals = [md_escape(v) for v in vals]
        lines.append("| " + " | ".join(escaped_vals) + " |\n")

    info_text = "**Award information**\n" + "".join(lines)
    return {"info_text": info_text}