# Bank Data API - Setup Guide

Complete setup documentation for the Bank Data API application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Option 1: Docker Setup (Recommended)](#option-1-docker-setup-recommended)
- [Option 2: Local Setup (Without Docker)](#option-2-local-setup-without-docker)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### For Docker Setup
- Docker Engine 20.10+
- Docker Compose v2.0+

### For Local Setup
- Python 3.12+
- pip (Python package manager)
- Git

---

## Option 1: Docker Setup (Recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd src-banks-trigger-app
```

### Step 2: Configure Environment (Optional)

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` to customize settings:

```bash
# Server Configuration
PORT=8080
HOST=0.0.0.0

# Logging Configuration
LOG_LEVEL=INFO          # Options: DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=detailed     # Options: simple, detailed, json

# Session Configuration
SESSION_TTL_MINUTES=30

# Rate Limiting
RATE_LIMIT_WINDOW_SECONDS=60
RATE_LIMIT_MAX_REQUESTS=10
```

### Step 3: Build and Run with Docker Compose

```bash
# Build and start the container
docker compose up --build

# Or run in detached mode (background)
docker compose up -d --build
```

### Step 4: Verify the Installation

```bash
# Check container status
docker compose ps

# Check logs
docker compose logs -f

# Test the API
curl http://localhost:8080/
```

### Docker Commands Reference

```bash
# Stop the container
docker compose down

# Restart the container
docker compose restart

# View logs
docker compose logs -f

# Rebuild after code changes
docker compose up -d --build

# Remove containers and volumes
docker compose down -v
```

### Alternative: Manual Docker Build

If you prefer not to use Docker Compose:

```bash
# Build the image
docker build -t bank-data-api .

# Run the container
docker run -d \
  --name bank-data-api \
  -p 8080:8080 \
  -e LOG_LEVEL=INFO \
  -e LOG_FORMAT=detailed \
  bank-data-api

# View logs
docker logs -f bank-data-api

# Stop the container
docker stop bank-data-api

# Remove the container
docker rm bank-data-api
```

### Custom Port Configuration

To run on a different port:

```bash
# Using Docker Compose - edit docker-compose.yml:
# ports:
#   - "9000:8080"  # Maps host port 9000 to container port 8080

# Using Docker run:
docker run -d -p 9000:8080 bank-data-api
```

---

## Option 2: Local Setup (Without Docker)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd src-banks-trigger-app
```

### Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your preferred settings
nano .env  # or use any text editor
```

### Step 5: Run the Application

```bash
python run.py
```

The server will start at `http://localhost:8080`.

### Step 6: Verify the Installation

```bash
# Test the API
curl http://localhost:8080/

# Open in browser
open http://localhost:8080/docs/
```

### Using the Start Script (Alternative)

A convenience script is available:

```bash
# Make executable (first time only)
chmod +x start.sh

# Run the application
./start.sh
```

The script will:
1. Create a virtual environment if it doesn't exist
2. Install dependencies
3. Start the application

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | `8080` | No |
| `HOST` | Server host | `0.0.0.0` | No |
| `FLASK_DEBUG` | Enable debug mode | `False` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `LOG_FORMAT` | Log format | `detailed` | No |
| `LOG_FILE` | Log file path | None (console) | No |
| `SESSION_TTL_MINUTES` | Session timeout | `30` | No |
| `RATE_LIMIT_WINDOW_SECONDS` | Rate limit window | `60` | No |
| `RATE_LIMIT_MAX_REQUESTS` | Max requests per window | `10` | No |

### Log Levels

- `DEBUG` - Detailed debug information
- `INFO` - General information (default)
- `WARNING` - Warning messages
- `ERROR` - Error messages only

### Log Formats

- `simple` - Basic log format: `LEVEL - message`
- `detailed` - Detailed format: `timestamp - logger - LEVEL - message`
- `json` - JSON structured logging (recommended for production)

---

## Verification

### Health Check

```bash
curl http://localhost:8080/
```

Expected response:
```json
{
  "message": "Bank Data API",
  "version": "1.3a"
}
```

### API Documentation

Open in browser: `http://localhost:8080/docs/`

### Test API Flow

1. **Initiate data request:**
```bash
curl -X GET "http://localhost:8080/citizen/1234567890/BankingData"
```

2. **Check session status** (use sessionID from step 1):
```bash
curl -X GET "http://localhost:8080/request/{sessionID}"
```

3. **Retrieve data:**
```bash
curl -X GET "http://localhost:8080/citizen/1234567890/BankingData/{sessionID}"
```

### Test PSNs

| PSN | Behavior |
|-----|----------|
| `1234567890` | Returns sample banking data |
| `9876543210` | Returns different banking data |
| `5555555555` | Returns all zero values |
| `1111111111` | Will deny consent |
| `3333333333` | Slow processing (PENDING state) |
| `0000000000` | No data available (404) |

---

## Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker compose logs

# Rebuild from scratch
docker compose down
docker compose build --no-cache
docker compose up
```

**Port already in use:**
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process or use a different port
docker compose down
# Edit docker-compose.yml to use a different port
docker compose up -d
```

### Local Setup Issues

**Python version mismatch:**
```bash
# Check Python version
python3 --version

# Ensure Python 3.12+
```

**Module not found errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Permission denied on start.sh:**
```bash
chmod +x start.sh
```

### Common Errors

**Connection refused:**
- Verify the application is running
- Check if the port is correct
- Ensure no firewall is blocking the port

**500 Internal Server Error:**
- Check application logs for details
- Verify environment configuration

---

## Support

For issues and questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review application logs
3. Consult the API documentation at `/docs/`
