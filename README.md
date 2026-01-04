# Weather AI Platform

Weather analytics platform built with **Django + FastAPI**.  
Provides real-time weather data with **optional AI-powered expert analysis**.  

The application is designed with a **microservice-style architecture**, feature flags, and graceful AI fallback.  

---

## Features

- Real-time weather data (OpenWeather API)
- Advanced weather metrics (wind chill, heat index)
- Optional AI-generated weather analysis
- Automatic fallback when AI is disabled or unavailable
- JWT authentication (Django → FastAPI)
- Feature flag support (`AI_PROVIDER`)
- HTMX-powered UI (no SPA framework)
- Fully Dockerized
- Auto-generated OpenAPI / Swagger docs

---

## Architecture

Browser  
  |  
  |-- Django (UI, Auth, Admin)  
  | |  
  | |-- JWT (HttpOnly cookies)  
  |  
  |-- FastAPI (Weather API, AI reports)  
  |  
  |-- OpenWeather API  
  |-- Optional AI Provider 

### services

project/  
  |- django_app/ # Auth, Admin, JWT  
  |- fastapi_app/ # Weather & AI API  
  |- docker-compose.yml  
  |- .env.example  
  |- README.md  


## Authentication Flow

- User logs in via Django  
- Django issues JWT (HttpOnly cookie)  
- FastAPI validates JWT using shared secret  
- Django Admin uses Django session auth  

---

## Quick start (Docker)

### Clone repository
```bash
git clone https://github.com/designbymalina/weather_ai.git
cd weather_ai
```

## Create environment file

```bash
cp .env.example .env
```

**Copy `.env.example` to `.env` and fill values.**  

DJANGO_SECRET_KEY=
OPENWEATHER_API_KEY=
OPENAI_API_KEY=  # optional
AI_PROVIDER=openai  # or "none"

## Run stack

```bash
docker compose up -d --build
```

## Services

**Service URL**

Django UI / Login: http://localhost:8001/login/  
Django Admin: http://localhost:8001/admin/  
FastAPI Docs: http://localhost:8000/docs  
FastAPI Health: http://localhost:8000/health  
PgAdmin: http://localhost:5050  

## Authentication

Login (local Postman / Django)

```bash
POST http://localhost:8001/api/auth/login/
```

Payload:

```json
{
  "username": "admin",
  "password": "password"
}
```

Response:

```json
{
  "access": "JWT_TOKEN",
  "refresh": "JWT_REFRESH"
}
```

Use access token in FastAPI Swagger -> Authorize:

```bash
Bearer <JWT_TOKEN>
```

## Weather API

Weather data provider: https://openweathermap.org/  

Fetch weather (no AI)

```bash
POST /api/v1/reports/weather
```

Example payload:

```json
{
  "name": "Warsaw"
}
```

Generate AI report (optional)

```bash
POST /api/v1/reports/generate
```

Requires AI_PROVIDER=openai and valid API key  
If AI is disabled or unavailable, API returns weather-only report  

## Configuration

| Variable | Description |
|----------|-------------|
| OPENWEATHER_API_KEY | Weather data provider |
| AI_PROVIDER | none / openai (groq, gemini) |
| OPENAI_API_KEY | Required if AI enabled |
| DATABASE_URL | PostgreSQL connection |
| DJANGO_SECRET_KEY | Shared JWT secret |

## Known Limitations

- No background task queue (Celery / RQ)  
- No rate limiting on API endpoints  
- AI usage billing is not handled  
- No long-term weather history storage  

## Development

Rebuild containers after env/code change:  

```bash
docker compose down
docker compose up -d --build
```

## License

MIT License  
