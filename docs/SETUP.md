# Bank Data API - Setup Guide

Complete setup documentation for the Bank Data API application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [1.1 Clone the Repository](#11-clone-the-repository)
- [1.2 Choose Your Setup Method](#12-choose-your-setup-method)
- [1.5 Configure Environment](#15-configure-environment)
- [1.6 Run the Server](#16-run-the-server)
- [1.7 Verify the Setup](#17-verify-the-setup)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| `Python 3.12+` | Python 3.12 or higher must be installed |
| `pip` | Python package manager (comes with Python) |
| `Git` | To clone the repository |
| `Docker` (optional) | If you prefer running via Docker instead of Python directly |

---

## 1.1 Clone the Repository

Get the [src-banks-trigger-app](https://github.com/InformationSystemsAgency/bank-declaration-api-mockup) repository onto your server:

```bash
git clone git@github.com:InformationSystemsAgency/bank-declaration-api-mockup.git
cd bank-declaration-api-mockup
```

---

## 1.2 Choose Your Setup Method

You can set up the application using either a **local Python environment** (recommended) or **Docker**.

### Option A: Local Python Setup (Recommended)

#### 1.3 Create a Virtual Environment

Isolate the project dependencies in a Python virtual environment:

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
# On Linux / macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

Alternatively, use the provided setup script which handles this automatically:

```bash
chmod +x setup_env.sh
./setup_env.sh
```

#### 1.4 Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This installs: Flask, Flask-CORS, PyYAML, Gunicorn, and python-dotenv.

### Option B: Docker Setup

Alternatively, if you have Docker installed, you can skip the Python setup above and run:

```bash
# Build and start the container
docker compose up --build -d
```

The server will start on port `8080`. Skip to **step 1.5** to configure your environment variables.

---

## 1.5 Configure Environment

Copy the example environment file and edit it for your bank:

```bash
# Copy the example config
cp .env.example .env

# Edit with your settings
nano .env
```

Or use the interactive setup script to generate it:

```bash
chmod +x setup_env.sh
./setup_env.sh
```

Key settings to configure in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Port the server will listen on |
| `HOST` | `0.0.0.0` | Bind to all interfaces so external connections work |
| `FLASK_DEBUG` | `false` | Set to `true` only during development |
| `LOG_LEVEL` | `INFO` | Logging verbosity: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `LOG_FORMAT` | `detailed` | Log output format: simple, detailed, or json |
| `SESSION_TTL_MINUTES` | `30` | How long sessions remain valid |
| `RATE_LIMIT_MAX_REQUESTS` | `10` | Maximum requests per rate-limit window |

---

## 1.6 Run the Server

**Option A: Using the start script**

```bash
chmod +x start.sh
./start.sh
```

This script automatically sets up the virtual environment, installs dependencies, and starts the server.

**Option B: Direct**

```bash
python run.py
```

The server will start on `http://0.0.0.0:8080` by default.

**Option C: With Gunicorn (production)**

```bash
gunicorn --bind 0.0.0.0:8080 --workers 4 "app:create_app()"
```

**Option D: With Docker**

```bash
docker compose up -d
```

---

## 1.7 Verify the Setup

Confirm everything is running correctly:

```bash
# From your server (local check):
curl http://localhost:8080/
```

If the setup is correct, you should see the API info page or a JSON response.
