import os
import logging
from datetime import datetime
from config import config

# Ruta absoluta al directorio de este fichero
base_dir = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel y creamos/entramos al directorio destino
logs_dir = os.path.join(base_dir, "..", config.LOGS_DIRECTORY)
os.makedirs(logs_dir, exist_ok=True)

# Obtenemos la fecha y hora actual
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Ruta al fichero
log_file = os.path.join(logs_dir, f'{timestamp}.log')

# Creamos el logger
logger = logging.getLogger("iptv_logger")

# Establecemos el nivel mínimo
log_level = getattr(logging, config.LOGS_LEVEL.upper(), logging.INFO)
logger.setLevel(log_level)

# Creamos el manejador de fichero
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Añadimos el manejador al logger
logger.addHandler(file_handler)