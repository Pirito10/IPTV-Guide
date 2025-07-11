import os
import logging
from datetime import datetime

from backend.config import config

# Ruta absoluta al directorio de este fichero
base_dir = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel y creamos/entramos al directorio destino
logs_dir = os.path.join(base_dir, "..", config.LOGS_DIRECTORY)
os.makedirs(logs_dir, exist_ok=True)

# Obtenemos la fecha y hora actual
timestamp = datetime.now().strftime(config.LOG_FILENAME_TIME_FORMAT)

# Ruta al fichero
log_file = os.path.join(logs_dir, f'{timestamp}.log')

# Creamos el logger
logger = logging.getLogger("iptv_logger")

# Establecemos el nivel mínimo
log_level = getattr(logging, config.LOGS_LEVEL.upper(), logging.INFO)
logger.setLevel(log_level)

# Desactivamos la propagación al logger raíz
logger.propagate = False

# Creamos el manejador de fichero
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(logging.Formatter(
    config.LOG_FORMAT,
    datefmt=config.LOG_DATE_FORMAT
))

# Añadimos el manejador al logger
logger.addHandler(file_handler)