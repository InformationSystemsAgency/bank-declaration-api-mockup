# Bank Data API

A Mockup application implementing the Bank Data API specification (version 1.3a) for secure data exchange between banks 
and the SRC (State Revenue Committee).

## Testing Environment

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

| Status | HTTP Code | Meaning |
|--------|-----------|---------|
| **PENDING** | 202 | Consent being acquired or data being prepared |
| **READY** | 200 | Data is available for retrieval |
| **EXPIRED** | 404 | Session expired or not found |
| **DENIED** | 590 | Citizen explicitly denied consent |

## Getting Started

1. **Set up locally** — see [Setup Guide](docs/SETUP.md)
2. **Connect to X-Road** — see [X-Road Deployment](docs/XROAD-DEPLOYMENT.md)
3. **Usage and testing** — see [Usage and Testing](docs/USAGE.md)
4. **Full API details and test data** — see [API Reference](docs/API.md)

## Quick Start

### Prerequisites

| Requirement | Details |
|-------------|---------|
| `Python 3.12+` | Python 3.12 or higher must be installed |
| `pip` | Python package manager (comes with Python) |
| `Git` | To clone the repository |
| `Docker` (optional) | If you prefer running via Docker instead of Python directly |

### Clone the Repository

```bash
git clone git@github.com:InformationSystemsAgency/bank-declaration-api-mockup.git
cd bank-declaration-api-mockup
```

### Option A: Local Python Setup

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Option B: Docker Setup

```bash
docker compose up --build -d
```

The server will start on `http://localhost:8080` by default.

### Verify the Setup

```bash
# From your server (local check):
curl http://localhost:8080/
```

If the setup is correct, you should see the API info page or a JSON response.

## Testing

### Sample PSNs for Testing

| PSN | Scenario |
|-----|----------|
| `1234567890` | Citizen with banking data (returns sample data) |
| `9876543210` | Different citizen with banking data |
| `5555555555` | Citizen with all zero values |
| `1111111111` | Citizen who will deny consent (DENIED state) |
| `3333333333` | Citizen with slow processing (demonstrates PENDING state) |
| `0000000000` | No data available (returns 404) |

### Direct API Calls (cURL)

**Initiate a data request:**
```bash
curl -X GET "http://<host>/citizen/1234567890/BankingData" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

**Check session status:**
```bash
curl -X GET "http://<host>/request/<sessionID>" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

**Retrieve banking data:**
```bash
curl -X GET "http://<host>/citizen/1234567890/BankingData/<sessionID>" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

## Response Data Fields

| Field | Description |
|-------|-------------|
| `DepositInterest` | Interest earned on deposits |
| `DebtSecurityInterest` | Interest from debt securities |
| `SecuritiesDeductable` | Deductible amount from securities |
| `NonPersonifiedIncome` | Non-personified income amount |

> **Note:** All fields are mandatory and must be >= 0. A value of `0` indicates no data is available or consent was not given for that field.

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Port the server will listen on |
| `HOST` | `0.0.0.0` | Bind to all interfaces |
| `FLASK_DEBUG` | `false` | Set to `true` only during development |
| `LOG_LEVEL` | `INFO` | Logging verbosity: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `LOG_FORMAT` | `detailed` | Log output format: simple, detailed, or json |
| `SESSION_TTL_MINUTES` | `30` | How long sessions remain valid |
| `RATE_LIMIT_MAX_REQUESTS` | `10` | Maximum requests per rate-limit window |

### Configuration File

```bash
cp .env.example .env
```

## Project Structure

```
bank-declaration-api-mockup/
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

## API Specification

The application serves the original OpenAPI specification at `/api-spec` (YAML) and `/api-spec.json` (JSON) endpoints.

## License

This is a prototype implementation for the X-Road data exchange project.
