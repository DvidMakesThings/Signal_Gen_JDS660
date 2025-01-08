import logging
from datetime import datetime
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup a logger"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Ensure the logs directory exists
log_dir = 'test/logs'
os.makedirs(log_dir, exist_ok=True)

# Create a logger for the test with a timestamped log file name
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_name = os.path.join(log_dir, f"test_log_{current_time}.log")
test_logger = setup_logger('test_logger', log_file_name)