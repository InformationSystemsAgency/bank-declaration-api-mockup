FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default environment variables
ENV PORT=8080
ENV HOST=0.0.0.0
ENV LOG_LEVEL=INFO

EXPOSE 8080

CMD ["python", "run.py"]
