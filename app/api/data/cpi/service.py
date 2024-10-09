from io import StringIO
from typing import List

import pandas as pd
import requests
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from .models import CPIEntry, CPIDataResponse


def determine_frequency(time_period):
    if 'Q' in time_period:
        return 'Q'
    elif any(month in time_period for month in
             ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]):
        return 'M'
    else:
        return 'Y'


def parse_quarter(date_str):
    year, quarter = date_str.split()
    quarter_month_map = {
        'Q1': '01',
        'Q2': '04',
        'Q3': '07',
        'Q4': '10'
    }
    month = quarter_month_map[quarter]
    return pd.Timestamp(f'{year}-{month}-01')


def parse_time_period(date_str: str, frequency: str) -> pd.Timestamp:
    if frequency == 'Q':
        return parse_quarter(date_str)
    elif frequency == 'M':
        return pd.to_datetime(date_str, format='%Y %b')
    else:
        return pd.to_datetime(date_str, format='%Y')


def conform_data(data: pd.DataFrame) -> JSONResponse:
    data.rename(columns={'TIME_PERIOD': 'time_period', 'OBS_VALUE': 'value', 'FREQ': 'frequency'}, inplace=True)
    data['frequency'] = data['time_period'].apply(determine_frequency)
    data['time_period'] = data['time_period'].str.replace('-', ' ')
    data['time_period'] = data.apply(lambda row: parse_time_period(row['time_period'], row['frequency']), axis=1)
    data = data[['time_period', 'value', 'frequency']]
    return data


def fetch_data_from_source(url: str, params: dict, skiprows: int = 0, names: List[str] = None) -> pd.DataFrame:
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = pd.read_csv(StringIO(response.text), skiprows=skiprows, names=names)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve data")


def get_cpi_data(country_code: str):
    if country_code.upper() == 'UK':
        request_url = "https://www.ons.gov.uk/generator"
        params = {
            'format': 'csv',
            'uri': '/economy/inflationandpriceindices/timeseries/l522/mm23'
        }
        skiprows = 8
        names = ['time_period', 'value']
    elif country_code.upper() == 'AU':
        request_url = "https://api.data.abs.gov.au/data/CPI/1.10001.10.50.Q"
        params = {
            'format': 'csv'
        }
        skiprows = 0
        names = None
    else:
        raise HTTPException(status_code=400, detail="Unsupported country code")

    data = fetch_data_from_source(request_url, params, skiprows, names)
    data = conform_data(data)
    cpi_entries = [CPIEntry(time_period=row['time_period'], value=row['value'], frequency=row['frequency']) for
                   index, row in data.iterrows()]
    return CPIDataResponse(data=cpi_entries)
