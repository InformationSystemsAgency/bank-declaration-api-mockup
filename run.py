"""
Main application entry point
Run this file to start the Bank Data API server
"""

from app import create_app
from app.config import Config, get_logger
import os

if __name__ == '__main__':
    app = create_app()
    config = Config()
    logger = get_logger('main')
    
    logger.info("="*60)
    logger.info("Bank Data API Server Starting")
    logger.info("="*60)
    logger.info(f"Host: {config.HOST}")
    logger.info(f"Port: {config.PORT}")
    logger.info(f"Debug: {config.DEBUG}")
    logger.info(f"Log Level: {config.LOG_LEVEL}")
    logger.info("")
    logger.info("Available endpoints:")
    logger.info("  GET  /                                          - API information")
    logger.info("  GET  /docs/                                     - Redoc Documentation")
    logger.info("  GET  /api-spec                                  - OpenAPI specification (YAML)")
    logger.info("  GET  /api-spec.json                             - OpenAPI specification (JSON)")
    logger.info("  GET  /citizen/{PSN}/BankingData                 - Initiate data request")
    logger.info("  GET  /request/{sessionID}                       - Check session status")
    logger.info("  GET  /citizen/{PSN}/BankingData/{sessionID}     - Retrieve banking data")
    logger.info("")
    logger.info("Example PSNs for testing:")
    logger.info("  1234567890 - Has banking data")
    logger.info("  9876543210 - Has different banking data")
    logger.info("  5555555555 - Has zero values") 
    logger.info("  1111111111 - Will deny consent")
    logger.info("  3333333333 - Slow processing (for demo)")
    logger.info("  0000000000 - No data available (404 error)")
    logger.info("")
    logger.info("Environment variables for configuration:")
    logger.info("  LOG_LEVEL - Set logging level (DEBUG, INFO, WARNING, ERROR)")
    logger.info("  LOG_FORMAT - Set log format (simple, detailed, json)")
    logger.info("  LOG_FILE - Optional log file path")
    logger.info("  PORT - Server port (default: 5000)")
    logger.info("  FLASK_DEBUG - Enable debug mode")
    logger.info("="*60)
    
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)