import logging
from logging.handlers import RotatingFileHandler
# from functools import wraps
# from time import perf_counter
import os


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str, filename: str):
    path = os.path.join(LOG_DIR, filename)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)


    formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    )


    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)


    file_handler = RotatingFileHandler(path, maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)


    if not logger.handlers:
        logger.addHandler(console)
        logger.addHandler(file_handler)
    return logger


# Global loggers
app_logger = get_logger("app", "app.log")
db_logger = get_logger("db", "db.log")


# Convenience wrappers
def log_info(msg: str):
    app_logger.info(msg)


def log_warn(msg: str):
    app_logger.warning(msg)


def log_error(msg: str):
    app_logger.error(msg)


def log_db(msg: str):
    db_logger.info(msg)
