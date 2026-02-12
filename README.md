# Bank Data API

A Flask application implementing the Bank Data API specification (version 1.3a) for secure data exchange between banks and the SRC (State Revenue Committee).

## Live Environment

- **Test Declaration Triggering App**: https://test-declaration.isaa.cloud/

## Overview

This application provides a REST API that allows the SRC to request banking data for citizens with proper consent management. The API is fully asynchronous and implements proper session management, rate limiting, and security features.

## API Endpoints

### Bank Operations
- `GET /citizen/{PSN}/BankingData` - Initiate data request for a citizen
- `GET /citizen/{PSN}/BankingData/{sessionID}` - Retrieve banking data
- `GET /request/{sessionID}` - Check session status

### Documentation
- `GET /docs/` - Interactive API documentation (Redoc)
- `GET /api-spec` - OpenAPI specification (YAML format)
- `GET /api-spec.json` - OpenAPI specification (JSON format)

## Session States

- **PENDING** (HTTP 202) - Consent being acquired or data being prepared
- **READY** (HTTP 200) - Data available for retrieval
- **EXPIRED** (HTTP 404) - Session expired or not found
- **DENIED** (HTTP 590) - Citizen explicitly denied consent

## Quick Start with Docker

The easiest way to run the application:

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t bank-mockup .
docker run -p 8080:8080 bank-mockup
```

The server will be available at `http://localhost:8080`.

## Local Installation

Prerequisites:
- Python 3.12+
- pip

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

The server will start on `http://localhost:8080` by default.

## Getting Started

1. **Set up locally** — see [Setup Guide](docs/SETUP.md)
2. **Connect to X-Road** — see [X-Road Deployment](docs/XROAD-DEPLOYMENT.md)
3. **Usage and testing** — see [Usage and Testing](docs/USAGE.md)
4. **Full API details and test data** — see [API Reference](docs/API.md)

## Testing

You can test the API using the hosted test environment or a local instance.

- **Testing UI**: https://test-declaration.isaa.cloud/
- **Local**: `http://localhost:8080` (see [Quick Start with Docker](#quick-start-with-docker) or [Local Installation](#local-installation))

### Sample PSNs for Testing

The application includes mock data for testing different scenarios:

| PSN | Behavior |
|-----|----------|
| `1234567890` | Returns sample banking data |
| `9876543210` | Returns different banking data |
| `5555555555` | Returns all zero values |
| `1111111111` | Will deny consent |
| `3333333333` | Slow processing (demonstrates PENDING state) |
| `0000000000` | No data available (returns 404) |

### Example API Flow

The examples below use the test environment URL. Replace `https://test-declaration.isaa.cloud` with `http://localhost:8080` for local testing.

1. **Initiate data request:**
```bash
curl -X GET "https://test-declaration.isaa.cloud/citizen/1234567890/BankingData" \
     -H "Authorization: Bearer <token>" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

Response:
```json
{
  "sessionID": "c1a35a20-427b-4492-904f-b91d9359cea1",
  "expiresAt": "2024-01-15T10:30:00Z"
}
```

2. **Check session status:**
```bash
curl -X GET "https://test-declaration.isaa.cloud/request/{sessionID}" \
     -H "Authorization: Bearer <token>" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

3. **Retrieve data (when status is READY):**
```bash
curl -X GET "https://test-declaration.isaa.cloud/citizen/1234567890/BankingData/{sessionID}" \
     -H "Authorization: Bearer <token>" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

Response:
```json
{
  "DepositInterest": 250000,
  "DebtSecurityInterest": 0,
  "SecuritiesDeductable": 45000,
  "NonPersonifiedIncome": 5640
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8080` |
| `HOST` | Server host | `0.0.0.0` |
| `FLASK_DEBUG` | Enable debug mode | `False` |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `LOG_FORMAT` | Log format (simple, detailed, json) | `detailed` |
| `LOG_FILE` | Optional log file path | Console only |
| `SESSION_TTL_MINUTES` | Session timeout | `30` |
| `RATE_LIMIT_WINDOW_SECONDS` | Rate limiting window | `60` |
| `RATE_LIMIT_MAX_REQUESTS` | Max requests per window | `10` |

### Configuration File

Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

### Docker Environment

Pass environment variables to Docker:
```bash
docker run -p 8080:8080 \
  -e LOG_LEVEL=DEBUG \
  -e LOG_FORMAT=json \
  bank-mockup
```

Or configure in `docker-compose.yml`:
```yaml
services:
  bank-mockup:
    build: .
    ports:
      - "8080:8080"
    environment:
      - LOG_LEVEL=DEBUG
      - LOG_FORMAT=json
```

## Project Structure

```
banks-declaration-mockup/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration management
│   ├── models/
│   │   └── __init__.py          # Data models and validation
│   ├── routes/
│   │   ├── core_routes.py       # Main API endpoints
│   │   ├── support_routes.py    # Session status endpoints
│   │   └── spec_routes.py       # OpenAPI specification endpoints
│   └── services/
│       ├── session_manager.py   # Session management logic
│       └── mock_data_service.py # Mock banking data service
├── static/
│   └── index.html               # Landing page
├── bank_data_api.yaml           # OpenAPI specification
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── Dockerfile                   # Docker build configuration
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # This file
```

## Security Considerations

This is a prototype implementation. In a production environment, consider:

- Authentication and authorization (OAuth 2.0, API keys)
- TLS/HTTPS encryption
- Database persistence for sessions and audit logs
- Rate limiting with Redis/database backend
- Input sanitization and validation
- Monitoring and alerting
- Load balancing and high availability

## API Specification

The application serves the original OpenAPI specification at `/api-spec` (YAML) and `/api-spec.json` (JSON) endpoints.

## License

This is a prototype implementation for the Central Bank of Armenia data exchange project.
