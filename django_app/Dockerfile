# django_app/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały projekt (w tym manage.py)
COPY . .

# Ustawienie zmiennej srodowiskowej: dev or prod
ARG DJANGO_ENV=dev

ENV DJANGO_SETTINGS_MODULE=config.settings_${DJANGO_ENV}

RUN if [ "$DJANGO_ENV" = "prod" ]; then \
    python manage.py collectstatic --noinput; \
fi

CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000"]
