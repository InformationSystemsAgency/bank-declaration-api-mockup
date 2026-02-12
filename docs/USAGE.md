# Usage and Testing Guide

This guide explains how to test the Bank Data API endpoints using the SRC Test Console or direct API calls.

---

## Testing Flow Overview

The Bank Data API follows a 3-step asynchronous flow:

### 1. Initiate Request

Send a request with a citizen's PSN (Personal Social Number). The API returns a `sessionID` to track the request.

```
POST /src/initiate
{"psn": "1234567890"}
```

### 2. Poll Status

Use the `sessionID` to check if the data is ready. Keep polling until the status changes from PENDING.

```
POST /src/poll
{"session_id": "<sessionID>"}
```

### 3. Retrieve Data

Once the status is READY, retrieve the actual banking data.

```
POST /src/retrieve
{"psn": "1234567890", "session_id": "<sessionID>"}
```

---

## Session States

| Status | HTTP Code | Meaning |
|--------|-----------|---------|
| **PENDING** | 202 | Consent being acquired or data being prepared |
| **READY** | 200 | Data is available for retrieval |
| **EXPIRED** | 404 | Session expired or not found |
| **DENIED** | 590 | Citizen explicitly denied consent |

---

## Sample Test PSNs

Use these PSN values to test different scenarios:

| PSN | Scenario |
|-----|----------|
| `1234567890` | Citizen with banking data (returns sample data) |
| `9876543210` | Different citizen with banking data |
| `5555555555` | Citizen with all zero values |
| `1111111111` | Citizen who will deny consent (DENIED state) |
| `3333333333` | Citizen with slow processing (demonstrates PENDING state) |
| `0000000000` | No data available (returns 404) |

---

## Using the Test Console

1. **Authenticate** — Enter your bank API token in the Authentication section on the Test Console page.
2. **Enter a PSN** — Type one of the sample PSNs above (e.g. `1234567890`) in the Citizen PSN field.
3. **Click "Initiate Request"** — The response panel will show the result and a `sessionID` will be populated automatically.
4. **Click "Poll Status"** — Check the session status. If PENDING, wait a moment and poll again.
5. **Click "Retrieve Data"** — Once the status is READY, retrieve the banking data. The full response will be displayed in the response panel.

---

## Direct API Calls (cURL)

You can also test the underlying bank API endpoints directly:

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

---

## Response Data Fields

| Field | Description |
|-------|-------------|
| `DepositInterest` | Interest earned on deposits |
| `DebtSecurityInterest` | Interest from debt securities |
| `SecuritiesDeductable` | Deductible amount from securities |
| `NonPersonifiedIncome` | Non-personified income amount |

> **Note:** All fields are mandatory and must be >= 0. A value of `0` indicates no data is available or consent was not given for that field.

---

## Next Steps

- For full API endpoint details, see the [API Reference](API.md)
- For X-Road integration, see the [X-Road Deployment Guide](XROAD-DEPLOYMENT.md)
