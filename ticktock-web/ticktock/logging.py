# Logging configuration for TickTock

import logging
import logging.config
from logging.handlers import RotatingFileHandler
from ticktock import config


def setup_logger(level: int = logging.INFO) -> None:
    # Configure the logger for TickTock
    logger = getLogger()
    logger.setLevel(level)

    ch_stream = logging.StreamHandler()
    ch_file = RotatingFileHandler(config.logfile, maxBytes=1_000_000, backupCount=4)
    logging.basicConfig(
        handlers=[ch_stream, ch_file],
        level=level,
        format="[%(asctime)s] (%(levelname)s) %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def getLogger() -> logging.Logger:
    return logging.getLogger("ticktock")
