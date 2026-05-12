import sys

from loguru import logger

from app.core.config import settings


LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:"
    "<cyan>{function}</cyan>:"
    "<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)


def setup_logger() -> None:
    """
    Configure centralized application logging.
    """

    logger.remove()

    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=settings.log_level,
        colorize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


setup_logger()