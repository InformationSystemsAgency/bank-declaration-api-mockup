"""
Bank Data API Application
A Flask application implementing the Bank Data API specification for data exchange between banks and SRC.
"""

from flask import Flask, request
from flask_cors import CORS
import os

def create_app():
    """Create and configure the Flask application."""
    # Set up logging first
    from app.config import setup_logging, get_logger, Config
    setup_logging()

    logger = get_logger('main')
    request_logger = get_logger('request')
    logger.info("Initializing Bank Data API application")

    app = Flask(__name__)

    # Enable CORS for all routes
    CORS(app)

    # Set Flask configuration from our config
    config = Config()
    app.config['DEBUG'] = config.DEBUG

    logger.info(f"Application configured - Debug: {config.DEBUG}")

    # Add request logging middleware for DEBUG level
    if config.LOG_LEVEL == 'DEBUG':
        @app.before_request
        def log_request_info():
            request_logger.debug("=" * 60)
            request_logger.debug(">>> INCOMING REQUEST")
            request_logger.debug(f">>> Method: {request.method}")
            request_logger.debug(f">>> URL: {request.url}")
            request_logger.debug(f">>> Path: {request.path}")

            # Log query parameters
            if request.args:
                request_logger.debug(f">>> Query Params: {dict(request.args)}")

            # Log headers (excluding sensitive ones)
            headers = {k: v for k, v in request.headers if k.lower() not in ['cookie', 'authorization']}
            request_logger.debug(f">>> Headers: {headers}")

            # Log request body for POST/PUT/PATCH
            if request.method in ['POST', 'PUT', 'PATCH']:
                if request.is_json:
                    try:
                        request_logger.debug(f">>> Body (JSON): {request.get_json()}")
                    except Exception:
                        request_logger.debug(">>> Body: [Could not parse JSON]")
                elif request.data:
                    request_logger.debug(f">>> Body (Raw): {request.data[:1000]}")  # Limit to 1000 chars

            request_logger.debug("=" * 60)

        @app.after_request
        def log_response_info(response):
            request_logger.debug("<<< RESPONSE")
            request_logger.debug(f"<<< Status: {response.status}")
            request_logger.debug("-" * 60)
            return response

        logger.info("Debug request logging enabled")
    
    # Register blueprints
    from app.routes.core_routes import core_bp
    from app.routes.support_routes import support_bp
    from app.routes.spec_routes import spec_bp
    
    app.register_blueprint(core_bp)
    app.register_blueprint(support_bp)
    app.register_blueprint(spec_bp)
    
    logger.info("All blueprints registered successfully")
    logger.info("Redoc documentation available at /docs/")
    
    return app