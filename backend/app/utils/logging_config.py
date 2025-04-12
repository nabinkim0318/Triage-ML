import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(debug=False):
    """Configure application logging"""
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
    )
    
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
    
        file_handler = RotatingFileHandler(
            'logs/app.log', 
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(log_level)
        
        error_handler = RotatingFileHandler(
            'logs/error.log', 
            maxBytes=10485760,
            backupCount=10
        )
        error_handler.setFormatter(logging.Formatter(log_format))
        error_handler.setLevel(logging.ERROR)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
    except (IOError, PermissionError):
        print("Warning: Unable to create log files. Using console logging only.")
    
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('uvicorn').setLevel(logging.WARNING)