# Weather AI Platform

AI-powered weather analytics platform built with **Django + FastAPI**, powered by external weather APIs and optional AI analysis.

---

## Features

- Weather data fetching (OpenWeather)
- Advanced weather metrics (wind chill, heat index)
- Optional AI-generated expert weather reports
- JWT authentication (Django -> FastAPI shared auth)
- PostgreSQL persistence
- Redis caching (optional)
- Fully Dockerized
- Auto-generated OpenAPI / Swagger docs

---

## Architecture

project/  
    |- django_app/ # Auth, Admin, JWT  
    |- fastapi_app/ # Weather & AI API  
    |- docker-compose.yml  
    |- .env.example  
    |- README.md  

**Auth flow**
- Django issues JWT tokens
- FastAPI validates JWT using shared secret

---

## Quick start (Docker)

### Clone repo
```bash
git clone https://github.com/artimman/weather_ai.git
cd weather_ai
```

## Create .env

```bash
cp .env.example .env
```

**Copy `.env.example` to `.env` and fill values.**  

DJANGO_SECRET_KEY  
OPENWEATHER_API_KEY  
optional OPENAI_API_KEY  

## Run stack

```bash
docker compose up -d --build
```

## Services

**Service URL**

Django Admin http://localhost:8001/admin  
FastAPI Docs http://localhost:8000/docs  
FastAPI Health http://localhost:8000/health  
PgAdmin http://localhost:5050  

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
  "name": "Warsaw",
  "lat": 52.2297,
  "lon": 21.0122
}
```

Generate AI report (optional)

```bash
POST /api/v1/reports/generate
```

Requires AI_PROVIDER=openai and valid API key  
Can be disabled with AI_PROVIDER=none  

## Configuration

| Variable | Description |
|----------|-------------|
| OPENWEATHER_API_KEY | Weather data provider |
| AI_PROVIDER | none, openai, groq, gemini |
| DATABASE_URL | PostgreSQL connection |
| DJANGO_SECRET_KEY | Shared JWT secret |

## Development

Rebuild containers after env/code change:  

```bash
docker compose down
docker compose up -d --build
```

## License

MIT License  
