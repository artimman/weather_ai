# django_app/weather/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WeatherReport(models.Model):
    """Stores reports produced by FastAPI AI pipeline"""
    report_id = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location_name = models.CharField(max_length=255)
    raw_payload = models.JSONField()
    summary = models.TextField()
    expert_notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.location_name} — {self.created_at.isoformat()}"
