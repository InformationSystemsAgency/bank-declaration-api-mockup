# Bank Data API Documentation

Welcome to the Bank Data API documentation.

## Live Environment

- **Test Declaration Triggering App**: https://test-declaration.isaa.cloud/

## Documentation Index

| Document | Description |
|----------|-------------|
| [Setup Guide](SETUP.md) | Complete installation and configuration guide |
| [X-Road Deployment](XROAD-DEPLOYMENT.md) | Deploy service into X-Road infrastructure |
| [Usage and Testing](USAGE.md) | Step-by-step usage and testing guide |
| [API Reference](API.md) | Full API endpoint details and test data |

## Quick Links

- **Live API Documentation**: Access the interactive API docs at `/docs/` endpoint when the application is running
- **OpenAPI Specification**: Available at `/api-spec` (YAML) and `/api-spec.json` (JSON)

## Getting Started

1. Set up the application locally — see [Setup Guide](SETUP.md)
2. Connect your local instance to X-Road — see [X-Road Deployment](XROAD-DEPLOYMENT.md)
3. Usage and testing — see [Usage and Testing](USAGE.md)
4. For all API details and test data — see [API Reference](API.md)

## Usage

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

### Basic API Flow

1. **Initiate a data request** using `GET /citizen/{PSN}/BankingData`
2. **Poll the session status** using `GET /request/{sessionID}`
3. **Retrieve the data** (once status is READY) using `GET /citizen/{PSN}/BankingData/{sessionID}`

See the [API Reference](API.md) for full endpoint details and examples.
