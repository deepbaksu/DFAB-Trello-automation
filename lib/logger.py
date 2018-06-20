#_*_ coding: utf-8 _*_

import logging
import logging.handlers
from config import LOG_FILENAME, LOG_FORMAT, LOGGER_NAME

DFAB_FORMAT = logging.Formatter(LOG_FORMAT)
DFAB_FILEHANDLER = logging.FileHandler(LOG_FILENAME)
DFAB_FILEHANDLER.setFormatter(DFAB_FORMAT)

LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.addHandler(DFAB_FILEHANDLER)
LOGGER.setLevel(logging.DEBUG)
