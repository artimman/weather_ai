# django_app/weather/services.py

import requests
from django.conf import settings

def request_report(location: str, requester=None):
    """Simple sync request to FastAPI to create/generate a report"""
    url = f"{settings.FASTAPI_BASE_URL}/api/v1/reports/generate"
    resp = requests.post(url, json={"location": location}, timeout=30)
    resp.raise_for_status()
    return resp.json() # expected { "report_id": "...", "status": "queued" }
