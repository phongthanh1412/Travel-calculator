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

    df = df.rename(columns={
        'ORIGIN_CITY_NAME': 'ORIGIN',
        'DESTINATION_CITY_NAME': 'DESTINATION',
        'YCA_FARE': 'ONE_WAY_FARE'
    })

    for col in ['ORIGIN', 'DESTINATION']:
        df[col] = df[col].astype(str).str.strip()

    df['ONE_WAY_FARE'] = df['ONE_WAY_FARE'].apply(sanitize_currency)
    return df

def get_airfare_origins(df):
    return ['-Select-'] + sorted(df['ORIGIN'].unique().tolist())

def get_airfare_destinations(df, origin):
    if origin == "-Select-":
        return []
    return sorted(df[df['ORIGIN'] == origin]['DESTINATION'].unique().tolist())

def lookup_airfare(df, origin, destination):
    row = df[(df['ORIGIN'] == origin) & (df['DESTINATION'] == destination)]
    if row.empty:
        return None
    return float(row.iloc[0]['ONE_WAY_FARE'])
