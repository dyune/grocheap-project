FROM python:3.12-slim

WORKDIR /backend_app

# Need GCC and some other things to successfully install requirements.txt within 3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend /backend_app/backend/

EXPOSE 8000

CMD ["uvicorn", "backend.application:app", "--host", "0.0.0.0", "--port", "8000"]