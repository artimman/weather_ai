# fastapi_app/app/models/report.py

from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from ..services.db import Base

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    report_id = Column(String(128), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    location_name = Column(String(255))
    raw_payload = Column(JSON)
    summary = Column(Text)
    expert_notes = Column(Text)
