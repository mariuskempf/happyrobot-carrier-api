"""Module for configuration of logging used in application."""

import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """Interception handler to make all logging entry unified structure and format."""

    def emit(self, record: logging.LogRecord):
        """Process log record.

        Args:
            record (LogRecord): Log record to be processed.
        """
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6  # pylint: disable=protected-access
        while frame and frame.f_code.co_filename == logging.__file__:
            if frame.f_back:
                frame = frame.f_back
                depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def apply_handling_custom_logger():
    """Define logging level of external modules.

    This sets log levels for noisy libraries. This ensures you won't drown in debug logs from
    dependencies.
    """
    logging.getLogger("httpx").setLevel(level=logging.INFO)
    logging.getLogger("httpcore").setLevel(level=logging.INFO)
    logging.getLogger("asyncio").setLevel(level=logging.INFO)
    logging.getLogger("uvicorn").setLevel(level=logging.INFO)
    logging.getLogger("botocore").setLevel(level=logging.INFO)
    logging.getLogger("urllib3").setLevel(level=logging.INFO)
    logging.getLogger("urllib3.connectionpool").setLevel(level=logging.INFO)
    # ...


def setup_logging(log_level: str | int, serialize=False):
    """Setup logging. Unify logging entry and collected handling over loguru module.

    This ensures every module's logs propagate to the root → intercepted by Loguru.
    No more:
        - duplicated logs
        - logs appearing twice
        - weird formatting differences

    Args:
        log_level (str | int): Loglevel.
        serialize (bool): Use Serialization form of output.
    """

    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level)

    # explicitly intercept Uvicorn's built-in loggers
    uvicorn_loggers = ("uvicorn", "uvicorn.error", "uvicorn.access")
    for name in uvicorn_loggers:
        uv_logger = logging.getLogger(name)
        uv_logger.handlers = []
        uv_logger.propagate = True

    # remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():  # pylint: disable=no-member
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(
        extra={"trace_id": "-"},  # default trace_id for all logs
        handlers=[
            {
                "sink": sys.stdout,
                "serialize": serialize,
                "level": log_level,
                # Note: format is only used when serialize=False.
                # When serialize=True, trace_id is included via extra field in JSON output.
                "format": (
                    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                    "<yellow>{level: <8}</yellow> | "
                    "<level>{extra[trace_id]}</level> | "
                    "<cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>"
                ),
            }
        ],
    )

    # handling custom logger
    apply_handling_custom_logger()
