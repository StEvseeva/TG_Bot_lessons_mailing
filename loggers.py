import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

FORMATTER = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
app_filename: Path = Path(os.getenv('LOG_FILENAME_PREFIX') + '_' + str(datetime.today().date()) + '.log')
error_filename: Path = Path(os.getenv('LOG_ERROR_PREFIX') + '_' + str(datetime.today().date()) + '.log')
log_path: Path = Path(os.getenv('LOG_PATH'))
APP_PATH: Path = log_path/app_filename
ERROR_PATH: Path = log_path/error_filename

logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
    filename=ERROR_PATH
)

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler
def get_file_handler():
   file_handler = TimedRotatingFileHandler(APP_PATH, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger