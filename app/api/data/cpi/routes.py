from fastapi import APIRouter, Depends
from . import service
from .models import CPIDataResponse
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/api",
)


@router.get('/cpi/{country_code}', response_model=CPIDataResponse)
async def get_cpi_data(country_code: str):
    return service.get_cpi_data(country_code=country_code)


@router.get('/economy/cpi/{country_code}', response_model=CPIDataResponse)
async def get_economy_data(country_code: str, db: Session = Depends(get_db)):
    return service.get_economy_data(vendor='ONS', ticker='CPI', attribute='CORE', frequency='Q',value_date=value_date)
