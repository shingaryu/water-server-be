import logging
import sys

FORMAT = '%(asctime)s [%(name)s][%(levelname)s] - %(message)s'
logging.basicConfig(format=FORMAT)

def get_logger(module_name, logger_level):
    logger = logging.getLogger(module_name)
    handler = logging.StreamHandler(sys.stdout)
    # logger.addHandler(handler)
    # LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
    if logger_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger