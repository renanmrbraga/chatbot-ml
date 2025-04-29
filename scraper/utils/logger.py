import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.config import LOGS_DIR  # import relativo

# Nome do arquivo de log baseado na data (YYYY-MM-DD)
log_file: Path = LOGS_DIR / f"chatppp_{datetime.now().strftime('%Y-%m-%d')}.log"


def get_logger(name: str = "chatppp") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler para terminal
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Handler para arquivo com rotação automática
        file_handler = RotatingFileHandler(
            str(log_file), maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.debug(f"📝 Logger '{name}' inicializado. Salvando logs em: {log_file}")

    return logger
