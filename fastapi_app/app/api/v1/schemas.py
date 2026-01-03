# fastapi_app/app/api/v1/schemas.py

from typing import Optional, Union

from pydantic import BaseModel, Field

# ===== INPUT =====


class LocationIn(BaseModel):
    name: str = Field(example="Warsaw")


# ===== METRICS =====


class MetricsOut(BaseModel):
    temperature: float
    wind_kph: float
    wind_chill: float
    heat_index: float


# ===== WEATHER =====


class WeatherCurrentOut(BaseModel):
    temp: float
    humidity: int
    wind_speed: float
    weather: list[dict]


class WeatherPayloadOut(BaseModel):
    current: WeatherCurrentOut


class WeatherOut(BaseModel):
    location: str
    metrics: MetricsOut
    weather: WeatherPayloadOut


# ===== HEALTH =====


class HealthOut(BaseModel):
    status: str


# ===== AI / FALLBACK RESPONSES =====


class WeatherOnlyOut(BaseModel):
    mode: str = "weather-only"
    location: str
    metrics: MetricsOut


class AIReportOut(BaseModel):
    mode: str = "ai"
    report_id: str
    summary: str
    expert_notes: Optional[str] = None


ReportResponse = Union[WeatherOnlyOut, AIReportOut]
