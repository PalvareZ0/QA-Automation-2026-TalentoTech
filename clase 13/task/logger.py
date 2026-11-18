"""
utils/logger.py — Logger centralizado del framework (Clase 13)

Escribe paso a paso en logs/suite.log (con rotación automática:
1 MB por archivo, guarda 5 históricos).

Uso en cualquier test o page object:

    from utils.logger import logger
    logger.info('Iniciando login con usuario: %s', 'standard_user')
"""
import logging
import pathlib
from logging.handlers import RotatingFileHandler

# 1) Carpeta donde se almacenan los logs (se crea si no existe)
LOGS_DIR = pathlib.Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# 2) Archivo rotativo: 1 MB por archivo, mantiene 5 históricos
#    (suite.log, suite.log.1, ... suite.log.5)
_handler = RotatingFileHandler(
    LOGS_DIR / "suite.log",
    maxBytes=1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
_handler.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s – %(message)s",
        datefmt="%H:%M:%S",
    )
)

# 3) Logger que usarán los tests
logger = logging.getLogger("talentolab")
logger.setLevel(logging.INFO)
logger.addHandler(_handler)
logger.propagate = False  # evita líneas duplicadas en la consola
