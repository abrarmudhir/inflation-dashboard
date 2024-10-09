from datetime import date

from pydantic import BaseModel
from typing import List
from sqlalchemy import String, Column, Date, Double

from app.database import Base


class CPIEntry(BaseModel):
    time_period: date
    value: float
    frequency: str


class CPIDataResponse(BaseModel):
    data: List[CPIEntry]


class TInflation(Base):
    __tablename__ = "t_inflation"

    id = Column(String, primary_key=True)
    vendor = Column(String)
    ticker = Column(String)
    attribute = Column(String)
    frequency = Column(String)
    value_date = Column(Date)
    value = Column(Double)
