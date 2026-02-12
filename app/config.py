"""
Configuration module for the Bank Data API
Handles logging configuration and application settings
"""

import os
import logging
import logging.config
from typing import Dict, Any

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads variables from .env file into os.environ
except ImportError:
    # python-dotenv not installed, will use system environment variables only
    pass


class Config:
    """Application configuration class"""
    
    # Server configuration
    PORT = int(os.environ.get('PORT', 8080))
    HOST = os.environ.get('HOST', '0.0.0.0')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    LOG_FORMAT = os.environ.get('LOG_FORMAT', 'detailed')  # 'simple', 'detailed', 'json'
    LOG_FILE = os.environ.get('LOG_FILE', None)  # Optional log file path
    
    # Session configuration
    SESSION_TTL_MINUTES = int(os.environ.get('SESSION_TTL_MINUTES', 30))
    
    # Rate limiting configuration
    RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get('RATE_LIMIT_WINDOW_SECONDS', 60))
    RATE_LIMIT_MAX_REQUESTS = int(os.environ.get('RATE_LIMIT_MAX_REQUESTS', 10))


def get_logging_config() -> Dict[str, Any]:
    """
    Get logging configuration dictionary based on environment settings
    """
    config = Config()
    
    # Define format strings
    formats = {
        'simple': '%(levelname)s - %(message)s',
        'detailed': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'json': '{"timestamp":"%(asctime)s","logger":"%(name)s","level":"%(levelname)s","message":"%(message)s","module":"%(module)s","function":"%(funcName)s","line":%(lineno)d}'
    }
    
    format_string = formats.get(config.LOG_FORMAT, formats['detailed'])
    
    # Base logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': format_string,
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': config.LOG_LEVEL,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            'app': {  # Our application logger
                'level': config.LOG_LEVEL,
                'handlers': ['console'],
                'propagate': False
            },
            'werkzeug': {  # Flask's logger
                'level': 'INFO',  # Always show werkzeug INFO messages
                'handlers': ['console'],
                'propagate': False
            },
            'flask': {
                'level': config.LOG_LEVEL,
                'handlers': ['console'],
                'propagate': False
            }
        },
        'root': {
            'level': config.LOG_LEVEL,
            'handlers': ['console']
        }
    }
    
    # Add file handler if log file is specified
    if config.LOG_FILE:
        logging_config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': config.LOG_LEVEL,
            'formatter': 'standard',
            'filename': config.LOG_FILE,
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5
        }
        
        # Add file handler to all loggers
        for logger_name in logging_config['loggers']:
            logging_config['loggers'][logger_name]['handlers'].append('file')
        logging_config['root']['handlers'].append('file')
    
    return logging_config


def setup_logging():
    """
    Set up logging configuration for the application
    """
    try:
        config = get_logging_config()
        logging.config.dictConfig(config)
        
        # Log the configuration being used
        logger = logging.getLogger('app.config')
        app_config = Config()
        
        logger.info("="*60)
        logger.info("Bank Data API - Logging Configuration")
        logger.info("="*60)
        logger.info(f"Log Level: {app_config.LOG_LEVEL}")
        logger.info(f"Log Format: {app_config.LOG_FORMAT}")
        logger.info(f"Log File: {app_config.LOG_FILE or 'Console only'}")
        logger.info(f"Debug Mode: {app_config.DEBUG}")
        logger.info("="*60)
        
        # Test that logging is working
        logger.debug("Debug logging is enabled")
        logger.info("Logging setup completed successfully")
        
    except Exception as e:
        # Fallback to basic logging if configuration fails
        print(f"Warning: Logging configuration failed: {e}")
        print("Falling back to basic logging...")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        logger = logging.getLogger('app.config')
        logger.warning("Using fallback logging configuration")


# Convenience function to get a logger with proper naming
def get_logger(name: str) -> logging.Logger:
    """
    Get a properly configured logger for the application
    """
    # Ensure logging is set up when logger is first requested
    logger = logging.getLogger(f'app.{name}')
    
    # If this is the first time getting a logger and no handlers are set up, 
    # set up basic logging as a fallback
    if not logger.handlers and not logging.getLogger('app').handlers:
        # Set up basic console logging as fallback
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        app_logger = logging.getLogger('app')
        app_logger.addHandler(console_handler)
        app_logger.setLevel(logging.INFO)
        app_logger.propagate = False
    
    return logger