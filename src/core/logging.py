import logging
import sys
import os
from datetime import datetime

def setup_logging():
    handlers = [logging.StreamHandler(sys.stdout)]
    
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    try:
        file_handler = logging.FileHandler(
            f'{log_dir}/app_{datetime.now().strftime("%Y%m%d")}.log', 
            encoding='utf-8'
        )
        handlers.append(file_handler)
    except (PermissionError, OSError):
        pass  # Fallback to console-only logging if file writing fails

    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def get_logger(name: str):
    return logging.getLogger(name)
