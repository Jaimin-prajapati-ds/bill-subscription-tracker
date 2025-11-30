"""Logging configuration for production."""
import logging
import logging.handlers
import os
from pathlib import Path

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

def setup_logging():
    """Setup production logging with rotation."""
    # Create logger
    logger = logging.getLogger("bill_tracker")
    logger.setLevel(logging.DEBUG)
    
    # Rotating file handler for errors
    error_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "error.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    
    # Rotating file handler for info
    info_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "info.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    info_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
