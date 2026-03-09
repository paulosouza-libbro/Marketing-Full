FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY assets/ ./assets/

WORKDIR /app/backend

EXPOSE ${PORT:-8000}
CMD sh -c "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"
