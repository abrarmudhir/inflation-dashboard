from datetime import date
from typing import List

from pydantic import BaseModel


class AnalyticsCPIEntry(BaseModel):
    time_period: date
    annualised_cpi: float


class AnalyticsCPIDataResponse(BaseModel):
    data: List[AnalyticsCPIEntry]
