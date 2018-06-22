#_*_ coding: utf-8 _*_

"""Logger"""
import logging
import logging.handlers
import config

DFAB_FORMAT = logging.Formatter(config.LOG_FORMAT)
DFAB_FILEHANDLER = logging.FileHandler(config.LOG_FILENAME)
DFAB_FILEHANDLER.setFormatter(DFAB_FORMAT)

LOGGER = logging.getLogger(config.LOGGER_NAME)
LOGGER.addHandler(DFAB_FILEHANDLER)
LOGGER.setLevel(logging.DEBUG)
