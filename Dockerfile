FROM python:3.11-slim

WORKDIR /app/backend

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/backend

# Install dependencies
COPY requirements.txt .
COPY requirements_rag.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements_rag.txt

# Copy project
COPY backend/ .
COPY rag/ ./rag/

# Run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
