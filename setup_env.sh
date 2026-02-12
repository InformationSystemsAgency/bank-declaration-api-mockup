#!/bin/bash

# Bank Data API - Environment Setup Script
# This script helps you create and configure your .env file

echo "Bank Data API - Environment Configuration Setup"
echo "==============================================="

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  A .env file already exists."
    echo "Current contents:"
    echo "---"
    cat .env
    echo "---"
    read -p "Do you want to overwrite it? (y/N): " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        echo "Cancelled. Your existing .env file is unchanged."
        exit 0
    fi
fi

echo ""
echo "Let's set up your environment configuration:"
echo ""

# Get environment type
echo "1. What environment is this for?"
echo "   1) Development (verbose logging, debug mode)"
echo "   2) Production (minimal logging, secure settings)"  
echo "   3) Testing (error-only logging, fast sessions)"
echo "   4) Custom (I'll configure manually)"
read -p "Choose (1-4) [1]: " env_type
env_type=${env_type:-1}

case $env_type in
    1)  # Development
        cat > .env << EOF
# Development Environment Configuration
PORT=5000
HOST=0.0.0.0
FLASK_DEBUG=true

LOG_LEVEL=DEBUG
LOG_FORMAT=detailed
LOG_FILE=logs/dev.log

SESSION_TTL_MINUTES=60
RATE_LIMIT_WINDOW_SECONDS=60
RATE_LIMIT_MAX_REQUESTS=20
EOF
        echo "✅ Created development .env configuration"
        ;;
    2)  # Production
        cat > .env << EOF
# Production Environment Configuration
PORT=8080
HOST=0.0.0.0
FLASK_DEBUG=false

LOG_LEVEL=WARNING
LOG_FORMAT=json
LOG_FILE=logs/bank_data_api.log

SESSION_TTL_MINUTES=30
RATE_LIMIT_WINDOW_SECONDS=60
RATE_LIMIT_MAX_REQUESTS=10
EOF
        echo "✅ Created production .env configuration"
        ;;
    3)  # Testing
        cat > .env << EOF
# Testing Environment Configuration
PORT=5001
HOST=127.0.0.1
FLASK_DEBUG=false

LOG_LEVEL=ERROR
LOG_FORMAT=simple

SESSION_TTL_MINUTES=5
RATE_LIMIT_WINDOW_SECONDS=10
RATE_LIMIT_MAX_REQUESTS=100
EOF
        echo "✅ Created testing .env configuration"
        ;;
    4)  # Custom
        echo ""
        echo "Creating custom configuration..."
        
        read -p "Server port [5000]: " port
        port=${port:-5000}
        
        read -p "Server host [0.0.0.0]: " host
        host=${host:-0.0.0.0}
        
        echo "Debug mode?"
        echo "  1) Enable (development)"
        echo "  2) Disable (production)"
        read -p "Choose (1-2) [2]: " debug_choice
        debug_choice=${debug_choice:-2}
        debug=$( [ "$debug_choice" = "1" ] && echo "true" || echo "false" )
        
        echo "Log level?"
        echo "  1) DEBUG (most verbose)"
        echo "  2) INFO (normal)"
        echo "  3) WARNING (important only)"
        echo "  4) ERROR (errors only)"
        read -p "Choose (1-4) [2]: " log_choice
        log_choice=${log_choice:-2}
        case $log_choice in
            1) log_level="DEBUG";;
            2) log_level="INFO";;
            3) log_level="WARNING";;
            4) log_level="ERROR";;
        esac
        
        echo "Log format?"
        echo "  1) Simple (level + message)"
        echo "  2) Detailed (timestamp + context)"
        echo "  3) JSON (structured)"
        read -p "Choose (1-3) [2]: " format_choice
        format_choice=${format_choice:-2}
        case $format_choice in
            1) log_format="simple";;
            2) log_format="detailed";;
            3) log_format="json";;
        esac
        
        read -p "Log to file? (leave empty for console only): " log_file
        
        read -p "Session timeout minutes [30]: " ttl
        ttl=${ttl:-30}
        
        # Create custom .env
        cat > .env << EOF
# Custom Environment Configuration
PORT=$port
HOST=$host
FLASK_DEBUG=$debug

LOG_LEVEL=$log_level
LOG_FORMAT=$log_format
EOF
        
        if [ ! -z "$log_file" ]; then
            echo "LOG_FILE=$log_file" >> .env
        fi
        
        cat >> .env << EOF

SESSION_TTL_MINUTES=$ttl
RATE_LIMIT_WINDOW_SECONDS=60
RATE_LIMIT_MAX_REQUESTS=10
EOF
        echo "✅ Created custom .env configuration"
        ;;
esac

echo ""
echo "📄 Your .env file contents:"
echo "=========================="
cat .env

echo ""
echo "🚀 Next steps:"
echo "1. Install dependencies: pip install -r requirements.txt"
echo "2. Start the API server: python run.py"
echo "3. The server will automatically use your .env settings"
echo ""
echo "📖 For more information, see ENV_USAGE_GUIDE.md"

# Create logs directory if LOG_FILE is specified
if grep -q "LOG_FILE=" .env && ! grep -q "^#.*LOG_FILE=" .env; then
    log_dir=$(grep "LOG_FILE=" .env | cut -d'=' -f2 | xargs dirname)
    if [ "$log_dir" != "." ] && [ ! -d "$log_dir" ]; then
        echo ""
        echo "📁 Creating logs directory: $log_dir"
        mkdir -p "$log_dir"
    fi
fi

echo ""
echo "⚠️  Security reminder:"
echo "   - Never commit .env files to version control"
echo "   - Add .env to your .gitignore file"
echo "   - Use different .env files for different environments"