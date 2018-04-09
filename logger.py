#_*_ coding: utf-8 _*_

import logging
import logging.handlers
from config import LOG_FILENAME, LOG_FORMAT, LOGGER_NAME

fomatter = logging.Formatter(LOG_FORMAT)
filehandler = logging.FileHandler(LOG_FILENAME)
filehandler.setFormatter(fomatter)

logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(filehandler)
logger.setLevel(logging.DEBUG)
