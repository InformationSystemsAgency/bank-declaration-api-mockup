# Bank Data API Reference

API specification for secure data exchange between banks and the SRC (State Revenue Committee).

## Base URL

```
http://localhost:8080
```

## Authentication

This prototype does not require authentication. In production, implement proper authentication (OAuth 2.0, API keys, etc.).

---

## Endpoints

### 1. Initiate Data Request

Initiates the data transfer process for a citizen.

**Endpoint:** `GET /citizen/{PSN}/BankingData`

**Parameters:**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| `PSN` | string | path | Yes | Personal Social Number (10 digits) |
| `X-Request-ID` | UUID | header | No | Request tracking identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8080/citizen/1234567890/BankingData" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

**Success Response (200):**

```json
{
  "sessionID": "c1a35a20-427b-4492-904f-b91d9359cea1",
  "expiresAt": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

| Code | Description |
|------|-------------|
| 400 | Invalid PSN format |
| 404 | Bank has no data for this citizen |

---

### 2. Check Session Status

Poll for the status of a data request.

**Endpoint:** `GET /request/{sessionID}`

**Parameters:**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| `sessionID` | UUID | path | Yes | Session identifier from initiate request |
| `X-Request-ID` | UUID | header | No | Request tracking identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8080/request/c1a35a20-427b-4492-904f-b91d9359cea1" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

**Response Codes:**

| Code | Status | Description |
|------|--------|-------------|
| 200 | READY | Data is ready for retrieval |
| 202 | PENDING | Consent being acquired or data being prepared |
| 404 | EXPIRED | Session expired or not found |
| 429 | - | Too many requests (rate limited) |
| 590 | DENIED | Citizen denied consent |

---

### 3. Retrieve Banking Data

Download citizen data after consent is granted.

**Endpoint:** `GET /citizen/{PSN}/BankingData/{sessionID}`

**Parameters:**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| `PSN` | string | path | Yes | Personal Social Number (10 digits) |
| `sessionID` | UUID | path | Yes | Session identifier |
| `X-Request-ID` | UUID | header | No | Request tracking identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8080/citizen/1234567890/BankingData/c1a35a20-427b-4492-904f-b91d9359cea1" \
     -H "X-Request-ID: 12345678-1234-1234-1234-123456789012"
```

**Success Response (200):**

```json
{
  "DepositInterest": 250000,
  "DebtSecurityInterest": 0,
  "SecuritiesDeductable": 45000,
  "NonPersonifiedIncome": 5640
}
```

**Error Responses:**

| Code | Description |
|------|-------------|
| 400 | Invalid PSN or sessionID format |
| 404 | PSN doesn't match session or session not ready |

---

## Data Models

### BankData

Banking data returned for a citizen.

| Field | Type | Description |
|-------|------|-------------|
| `DepositInterest` | number | Interest from deposits (minimum: 0) |
| `DebtSecurityInterest` | number | Interest from debt securities (minimum: 0) |
| `SecuritiesDeductable` | number | Securities deductible amount (minimum: 0) |
| `NonPersonifiedIncome` | number | Non-personified income (minimum: 0) |

**Note:** All fields are mandatory. Zero values indicate either no such income or consent not given for that specific data element.

### PSN Format

- Exactly 10 digits
- Pattern: `^[0-9]{10}$`
- Example: `1234567890`

### UUID Format

- Standard UUID v4 format
- Pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$`
- Example: `c1a35a20-427b-4492-904f-b91d9359cea1`

---

## Session Lifecycle

```
                    ┌─────────────┐
                    │   INITIATE  │
                    │   Request   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   PENDING   │
                    │  (HTTP 202) │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
       ┌───────────┐ ┌───────────┐ ┌───────────┐
       │   READY   │ │  EXPIRED  │ │  DENIED   │
       │ (HTTP 200)│ │ (HTTP 404)│ │ (HTTP 590)│
       └─────┬─────┘ └───────────┘ └───────────┘
             │
             ▼
       ┌───────────┐
       │  RETRIEVE │
       │   Data    │
       └───────────┘
```

---

## Rate Limiting

Default configuration:
- **Window:** 60 seconds
- **Max Requests:** 10 per window

When rate limited, the API returns HTTP 429 (Too Many Requests).

---

## Test Data

For testing purposes, use these PSNs:

| PSN | Behavior |
|-----|----------|
| `1234567890` | Returns sample banking data |
| `9876543210` | Returns different banking data |
| `5555555555` | Returns all zero values |
| `1111111111` | Denies consent (HTTP 590) |
| `3333333333` | Slow processing (stays PENDING) |
| `0000000000` | No data available (HTTP 404) |

---

## OpenAPI Specification

Access the full OpenAPI specification:

- **YAML format:** `GET /api-spec`
- **JSON format:** `GET /api-spec.json`
- **Interactive docs:** `GET /docs/`
