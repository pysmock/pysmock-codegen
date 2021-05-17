import logging
import sys
APP_LOGGER_NAME="pysmock-codegen"
def set_app_level_logger(logger_name=APP_LOGGER_NAME, file_name = None, log_level=logging.INFO):
    APP_LOGGER_NAME = logger_name
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(stream_handler)
    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def get_logger(module_name):    
   return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
