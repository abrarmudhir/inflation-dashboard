import pandas as pd
from fastapi import APIRouter
from app.api.data.cpi import service as data_service
from . import service as analytics_service
from .models import AnalyticsCPIDataResponse

router = APIRouter(
    prefix="/api",
)


@router.get('/annualised_cpi/{country_code}', response_model=AnalyticsCPIDataResponse)
async def get_annualised_cpi(country_code: str):
    cpi = data_service.get_cpi_data(country_code=country_code)
    cpi_df = pd.DataFrame([entry.dict() for entry in cpi.data])
    annualised_cpi = analytics_service.calculate_annualised_cpi(data=cpi_df)
    return annualised_cpi
