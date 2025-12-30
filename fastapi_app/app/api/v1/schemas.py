# fastapi_app/app/api/v1/schemas.py

from pydantic import BaseModel, Field
from typing import Any, Dict

class LocationIn(BaseModel):
    name: str = Field(example="Warsaw")
    lat: float = Field(example=52.2297)
    lon: float = Field(example=21.0122)


class WeatherMetrics(BaseModel):
    temperature: float
    wind_kph: float
    wind_chill: float
    heat_index: float


class WeatherOut(BaseModel):
    location: str
    metrics: WeatherMetrics
    weather: Dict[str, Any]


class ReportOut(BaseModel):
    report_id: str
    summary: str
