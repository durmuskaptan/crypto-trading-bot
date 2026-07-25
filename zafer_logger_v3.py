import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class ZaferLogger:
    def __init__(self, log_file='zafer_bot.log', max_bytes=10*1024*1024, backup_count=5):
        self.logger = logging.getLogger('ZaferBot')
        self.logger.setLevel(logging.DEBUG)
        
        # Format
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = RotatingFileHandler(
            f'logs/{log_file}',
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        return self.logger

logger = ZaferLogger().get_logger()