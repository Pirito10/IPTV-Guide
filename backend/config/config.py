# IP y puerto de la interfaz donde escuchará el servidor
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

# Horas a las que actualizar la guía EPG
EPG_SCHEDULER_HOURS = "10,14,18,22"

# Enlaces a los ficheros de la lista M3U y la guía EPG
M3U_URL = "http://127.0.0.1:43110/1JKe3VPvFe35bm1aiHdD4p1xcGCkZKhH3Q/data/listas/lista_fuera_iptv.m3u"
EPG_URL = "https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guiatv.xml"

# Nombre del directorio donde guardar los logs
LOGS_DIRECTORY = "logs"
# Nivel mínimo de los logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOGS_LEVEL = "INFO"

# Nombre del directorio donde guardar copias de los ficheros descargados
BACKUP_DIRECTORY = "data"
# Nombres de los ficheros
EPG_BACKUP = "epg_backup.xml"
M3U_BACKUP = "m3u_backup.m3u"

# ID por defecto para los canales con ID desconocido
DEFAULT_ID = "unknown"

# Temporizador (en segundos) de espera antes de volver a descargar la lista M3U
M3U_DOWNLOAD_TIMER = 1800

# Cantidad de reintentos de descarga de la guía EPG
EPG_MAX_RETRIES = 3
# Cantidad (en minutos) a incrementar al temporizador después de cada reintento
RETRY_INCREMENT = 30

# Timeouts (en segundos) para las descargas de ficheros y logos
FILE_TIMEOUT = 10
LOGO_TIMEOUT = 2

# Tiempo (en horas) para considerar válida una entrada en la caché de los logos
LOGO_TTL = 4
# Tiempo (en minutos) para considerar inválida una entrada en la caché de los logos
INVALID_LOGO_TTL = 1
# Variación aleatoria (en porcentaje) para el TTL de los logos
LOGO_JITTER = 0.1

# Prefijo de la URL de la API
API_BASE_PATH = "/api"

# Rutas de la API
CHANNELS_ROUTE = "/channels"
EPG_ROUTE = "/epg"
HEALTH_ROUTE = "/health"

# Formato y fecha de los logs
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILENAME_TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"