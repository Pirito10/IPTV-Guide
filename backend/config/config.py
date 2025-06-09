# ==================
# 📡 Servidor y API
# ==================

# IP y puerto donde escuchará el servidor de desarrollo Flask
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

# Prefijo base de las rutas de la API
API_BASE_PATH = "/api"

# Subrutas de la API
CHANNELS_ROUTE = "/channels"
EPG_ROUTE = "/epg"
HEALTH_ROUTE = "/health"


# ==============================
# 🔗 Enlaces a fuentes de datos
# ==============================

# URLs de los ficheros de la lista M3U y la guía EPG
M3U_URL = "http://127.0.0.1:43110/1JKe3VPvFe35bm1aiHdD4p1xcGCkZKhH3Q/data/listas/lista_fuera_iptv.m3u"
EPG_URL = "https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guiatv.xml"


# ============================
# 💾 Almacenamiento y backups
# ============================

# Directorio donde se guardan copias de los ficheros descargados
BACKUP_DIRECTORY = "data"

# Nombres de los ficheros de respaldo
EPG_BACKUP = "epg_backup.xml"
M3U_BACKUP = "m3u_backup.m3u"


# ===================================
# 📅 Planificación y actualizaciones
# ===================================

# Horas a las que se actualizará la guía EPG
EPG_SCHEDULER_HOURS = "10,14,18,22"

# Tiempo mínimo (en segundos) entre dos descargas de la lista M3U
M3U_DOWNLOAD_TIMER = 1800

# Número máximo de reintentos al fallar la descarga de la guía EPG
EPG_MAX_RETRIES = 3

# Incremento de espera (en minutos) entre reintentos consecutivos
RETRY_INCREMENT = 30


# ============
# ⏱️ Timeouts
# ============

# Timeout (en segundos) para la descarga de ficheros
FILE_TIMEOUT = 10

# Timeout (en segundos) para la comprobación de logos
LOGO_TIMEOUT = 2


# =================
# 🖼️ Logos y caché
# =================

# Tiempo (en horas) para considerar válido un logo en caché
LOGO_TTL = 4

# Tiempo (en minutos) para mantener en caché un logo no válido
INVALID_LOGO_TTL = 1

# Porcentaje de variación aleatoria sobre el TTL de los logos
LOGO_JITTER = 0.1


# ========
# 📝 Logs
# ========

# Directorio donde se guardan los archivos de log
LOGS_DIRECTORY = "logs"

# Nivel mínimo del log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOGS_LEVEL = "INFO"

# Formato de los mensajes del log
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILENAME_TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


# =============
# ⚙️ Generales
# =============

# ID por defecto para los sin ID
DEFAULT_ID = "unknown"

# Días hacia adelante para los que se cargan programas
EPG_MAX_DAYS = 2