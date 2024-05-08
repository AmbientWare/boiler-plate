# Custom Logger Using Loguru

import logging
import sys
from pathlib import Path
from loguru import logger

# import json


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        if "/health" in record.getMessage():
            return

        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls, logging_config: dict):
        logger = cls.customize_logging(  # type: ignore
            logging_config.get("path", "/tmp/app/logs"),
            level=logging_config.get("level", "info"),
            retention=logging_config.get("retention", "7 days"),
            rotation=logging_config.get("rotation", "7 days"),
            format=logging_config.get(
                "format",
                "<level>{level: <8}</level> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>)",
            ),
        )
        return logger

    @classmethod
    def customize_logging(
        cls, filepath: Path, level: str, rotation: str, retention: str, format: str
    ):
        logger.remove()
        logger.add(
            sys.stdout, enqueue=True, backtrace=True, level=level.upper(), format=format
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]
        return logger.bind(request_id=None, method=None)

    # @classmethod
    # def load_logging_config(cls, config_path):
    #     config = None
    #     with open(config_path) as config_file:
    #         config = json.load(config_file)
    #     return config
