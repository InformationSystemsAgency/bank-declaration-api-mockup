# Using .env Files with Bank Data API

The Bank Data API supports configuration through `.env` files using the `python-dotenv` library. This allows you to set configuration without modifying code or setting system environment variables.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
This will install `python-dotenv` along with other dependencies.

### 2. Create Your .env File
```bash
# Copy the example file
cp .env.example .env

# Or copy the dev.env file
cp dev.env .env

# Edit with your preferred settings
nano .env
```

### 3. Run the Application
```bash
python run.py
```
The application will automatically load settings from the `.env` file.

## How It Works

### Automatic Loading
The `app/config.py` file automatically loads your `.env` file when the application starts:

```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file into os.environ
```

### Configuration Priority (Highest to Lowest)
1. **System Environment Variables** - `export LOG_LEVEL=DEBUG`
2. **`.env` File Variables** - Settings in your `.env` file
3. **Default Values** - Built-in defaults in the code

## .env File Examples

### Development Configuration
```bash
# .env file for development
PORT=5000
HOST=0.0.0.0
FLASK_DEBUG=true

LOG_LEVEL=DEBUG
LOG_FORMAT=detailed
LOG_FILE=logs/dev.log

SESSION_TTL_MINUTES=60
```

### Production Configuration
```bash
# .env file for production
PORT=8080
HOST=0.0.0.0
FLASK_DEBUG=false

LOG_LEVEL=WARNING
LOG_FORMAT=json
LOG_FILE=/var/log/bank_data_api.log

SESSION_TTL_MINUTES=30
RATE_LIMIT_MAX_REQUESTS=5
```

### Testing Configuration
```bash
# .env file for testing
PORT=5001
LOG_LEVEL=ERROR
LOG_FORMAT=simple
SESSION_TTL_MINUTES=10
```

## Available Configuration Variables

### Server Settings
```bash
PORT=5000              # Server port
HOST=0.0.0.0          # Server host (0.0.0.0 for all interfaces)
FLASK_DEBUG=false     # Enable Flask debug mode (true/false)
```

### Logging Settings
```bash
LOG_LEVEL=INFO        # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=detailed   # simple, detailed, json
LOG_FILE=logs/app.log # Optional: log to file (comment out for console only)
```

### Application Settings
```bash
SESSION_TTL_MINUTES=30           # How long sessions last
RATE_LIMIT_WINDOW_SECONDS=60     # Rate limiting time window
RATE_LIMIT_MAX_REQUESTS=10       # Max requests per time window
```

## Different Ways to Use Configuration

### Method 1: .env File (Recommended)
```bash
# Create .env file
echo "LOG_LEVEL=DEBUG" > .env
echo "PORT=5000" >> .env

# Run application (automatically loads .env)
python run.py
```

### Method 2: System Environment Variables
```bash
# Set environment variables
export LOG_LEVEL=DEBUG
export PORT=5000

# Run application
python run.py
```

### Method 3: Inline Environment Variables
```bash
# Set variables for single run
LOG_LEVEL=DEBUG PORT=5000 python run.py
```

### Method 4: Multiple .env Files
```bash
# Different files for different environments
cp .env.example .env.development
cp .env.example .env.production

# Load specific file (modify config.py to specify file)
```

## Managing Multiple Environments

### Development
```bash
# .env.development
PORT=5000
LOG_LEVEL=DEBUG
LOG_FORMAT=detailed
FLASK_DEBUG=true
```

### Testing  
```bash
# .env.testing
PORT=5001
LOG_LEVEL=ERROR
LOG_FORMAT=simple
FLASK_DEBUG=false
```

### Production
```bash
# .env.production
PORT=8080
LOG_LEVEL=WARNING
LOG_FORMAT=json
LOG_FILE=/var/log/app.log
FLASK_DEBUG=false
```

### Switching Environments
```bash
# Copy the appropriate env file
cp .env.development .env    # For development
cp .env.production .env     # For production

# Or use symbolic links
ln -sf .env.development .env
```

## Validation and Debugging

### Check What Values Are Loaded
The application logs its configuration on startup:
```
2025-10-10 12:00:00 - app.config - INFO - ============================================================
2025-10-10 12:00:00 - app.config - INFO - Bank Data API - Logging Configuration
2025-10-10 12:00:00 - app.config - INFO - ============================================================
2025-10-10 12:00:00 - app.config - INFO - Log Level: DEBUG
2025-10-10 12:00:00 - app.config - INFO - Log Format: detailed
2025-10-10 12:00:00 - app.config - INFO - Log File: Console only
2025-10-10 12:00:00 - app.config - INFO - Debug Mode: True
```

### Verify Environment Loading
```python
# Add this to config.py for debugging
import os
print("Environment variables:")
for key in ['PORT', 'LOG_LEVEL', 'LOG_FORMAT']:
    print(f"  {key} = {os.environ.get(key, 'NOT SET')}")
```

## Common Patterns

### Docker Usage
```dockerfile
# Dockerfile
COPY .env.production .env
CMD ["python", "run.py"]
```

### Docker Compose
```yaml
# docker-compose.yml
services:
  api:
    build: .
    env_file: .env.production
    ports:
      - "8080:8080"
```

### Kubernetes
```yaml
# ConfigMap from .env file
kubectl create configmap app-config --from-env-file=.env
```

## Security Notes

### ⚠️ Important Security Guidelines

1. **Never commit `.env` files to git:**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore
```

2. **Use different files for different environments:**
```bash
.env.example     # Template (safe to commit)
.env.development # Development settings  
.env.production  # Production settings (never commit)
.env             # Current active settings (never commit)
```

3. **Validate sensitive settings:**
```python
# In production, ensure secure values
if os.environ.get('FLASK_DEBUG', '').lower() == 'true':
    if os.environ.get('ENV') == 'production':
        raise ValueError("Debug mode cannot be enabled in production!")
```

## Troubleshooting

### .env File Not Loading
1. Check that `python-dotenv` is installed: `pip install python-dotenv`
2. Ensure `.env` file is in the same directory as `run.py`
3. Check file permissions: `chmod 644 .env`
4. Verify no syntax errors in `.env` file

### Variables Not Taking Effect
1. Check spelling of variable names
2. Verify no spaces around `=`: Use `PORT=5000` not `PORT = 5000`
3. System environment variables override `.env` file values
4. Check the startup logs to see what values are actually loaded

### File Not Found
```bash
# Check if .env exists
ls -la .env

# Create from example
cp .env.example .env
```

This system gives you maximum flexibility for configuration management across different environments!