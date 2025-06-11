FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=app.settings
CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]