# fastapi_app/app/ai/pipeline.py

import uuid

from openai import AuthenticationError, OpenAIError, RateLimitError
from sqlalchemy.orm import Session

from ..ai.providers import get_provider
from ..core import AI_PROVIDER, OPENAI_API_KEY
from ..core.config import get_ai_provider
from ..models.report import Report
from ..services.geocoding import geocode_city
from ..services.metrics import compute_heat_index, compute_wind_chill
from ..services.weather_fetcher import fetch_weather_openweather, normalize_weather


async def generate_full_report(location_q: dict, db: Session):
    lat, lon = await geocode_city(location_q.get("name"))

    raw = await fetch_weather_openweather(lat, lon)
    normalized = await normalize_weather(raw)

    current = normalized["current"]
    temp = current.get("temp")
    wind_ms = current.get("wind_speed", 0)
    wind_kph = wind_ms * 3.6

    wc = compute_wind_chill(temp, wind_kph)
    hi = compute_heat_index(temp, current.get("humidity", 0))

    ai_provider = get_ai_provider()

    # ===== TRYB BEZ AI =====
    # if AI_PROVIDER in ("none", "", None):
    if ai_provider in ("none", "", None):
        return {
            "mode": "weather-only",
            "location": location_q.get("name"),
            "metrics": {
                "temperature": temp,
                "wind_kph": round(wind_kph, 1),
                "wind_chill": wc,
                "heat_index": hi,
            },
            "weather": normalized,
        }

    # ===== AI MODE =====

    try:
        prompt = f"""
        You are a professional meteorologist and weather risk analyst.

        Analyze the following weather conditions for a real human user.

        Location: {location_q.get("name")}
        Temperature: {temp}°C
        Wind speed: {wind_kph:.1f} km/h
        Wind chill: {wc}°C
        Heat index: {hi}°C
        Humidity: {current.get("humidity")}%

        Your task:
        1. Explain how the weather feels to a human.
        2. Identify any risks or discomfort.
        3. Give practical advice (clothing, outdoor activity).
        4. End with a short, clear summary sentence.

        Tone:
        - clear
        - expert
        - human-friendly
        - no emojis
        - no markdown
        """

        provider = get_provider(AI_PROVIDER, OPENAI_API_KEY)
        ai_text = provider.generate(prompt, max_tokens=500, temperature=0.2)

        report = Report(
            report_id=str(uuid.uuid4()),
            location_name=location_q.get("name"),
            raw_payload=normalized,
            summary=ai_text.split("\n\n")[0] if ai_text else "",
            expert_notes=ai_text,
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return {
            "mode": "ai",
            "report_id": report.report_id,
            "summary": report.summary,
        }

    except RateLimitError:
        return {
            "mode": "ai-disabled",
            "reason": "insufficient_quota",
            "message": "There are no funds in your OpenAI account. Please top up your account.",
            "location": location_q.get("name"),
            "metrics": {
                "temperature": temp,
                "wind_kph": round(wind_kph, 1),
                "wind_chill": wc,
                "heat_index": hi,
            },
        }

    except AuthenticationError:
        return {
            "mode": "ai-disabled",
            "reason": "invalid_api_key",
            "message": "Invalid OpenAI key.",
        }

    except OpenAIError:
        return {
            "mode": "ai-disabled",
            "reason": "ai_unavailable",
            "message": "The AI service is temporarily unavailable.",
        }
