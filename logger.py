#_*_ coding: utf-8 _*_

import logging
import logging.handlers
from config import log_filename, log_format, logger_name

fomatter = logging.Formatter(log_format)
filehandler = logging.FileHandler(log_filename)
filehandler.setFormatter(fomatter)

logger = logging.getLogger(logger_name)
logger.addHandler(filehandler)
logger.setLevel(logging.DEBUG)
