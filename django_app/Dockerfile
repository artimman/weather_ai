# django_app/Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały projekt (w tym manage.py)
COPY . .

# Instalacja collectstatic (/admin - CSS itp.)
RUN python manage.py collectstatic --noinput

# CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000", "-w", "4"]
