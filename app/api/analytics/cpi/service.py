import pandas as pd
from fastapi import HTTPException

from .models import AnalyticsCPIDataResponse, AnalyticsCPIEntry


def calculate_annualised_cpi(data: pd.DataFrame, frequency: str = 'Q') -> AnalyticsCPIDataResponse:
    if frequency != 'Q':
        raise HTTPException(status_code=400, detail=f"Unsupported frequency({frequency!r}). Only quarterly('Q') data "
                                                    f"is supported.")
    if data.empty:
        raise HTTPException(status_code=400, detail="No CPI data available for calculation")

    quarterly_data = data[data['frequency'] == 'Q']

    if quarterly_data.empty:
        raise HTTPException(status_code=400, detail="No quarterly CPI data available for calculation")

    quarterly_data.loc[:, 'time_period'] = pd.to_datetime(quarterly_data['time_period'], format="%Y %b",
                                                          errors='coerce')

    quarterly_data = quarterly_data.dropna(subset=['time_period'])  # Drop rows with invalid dates
    quarterly_data = quarterly_data.sort_values(by='time_period')

    annualised_cpi_entries = []
    for index, row in quarterly_data.iterrows():
        current_date = row['time_period']
        current_value = row['value']

        one_year_ago_date = current_date - pd.DateOffset(years=1)
        one_year_ago_cpi = quarterly_data[quarterly_data['time_period'] == one_year_ago_date]

        if one_year_ago_cpi.empty:
            continue

        one_year_ago_value = one_year_ago_cpi['value'].values[0]
        annualised_inflation_rate = (current_value - one_year_ago_value) / one_year_ago_value

        entry = AnalyticsCPIEntry(time_period=current_date.date(), annualised_cpi=annualised_inflation_rate)
        annualised_cpi_entries.append(entry)

    return AnalyticsCPIDataResponse(data=annualised_cpi_entries)

