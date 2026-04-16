import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger():
    logging.basicConfig( 
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers = [RotatingFileHandler(
            "logs/app.log",
            maxBytes=10 * 1024 * 1024,  
            backupCount=5 
        ),
        logging.StreamHandler()] # 콘솔 터미널에 로그 출력
        )