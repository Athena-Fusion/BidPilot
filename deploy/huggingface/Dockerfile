FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MOCK_MODE=true \
    BACKEND_HOST=0.0.0.0 \
    BACKEND_PORT=7860 \
    DATA_DIR=/app/backend/data \
    OUTPUT_DIR=/app/backend/data/outputs

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend /app/backend

EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860", "--proxy-headers", "--forwarded-allow-ips", "*"]
