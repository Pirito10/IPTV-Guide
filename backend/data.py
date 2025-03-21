# Enlaces a los archivos
EPG_URL = "https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guiatv.xml"
M3U_URL = "http://127.0.0.1:43110/1H3KoazXt2gCJgeD8673eFvQYXG7cbRddU/lista-ace.m3u"

# Variables para almacenamiento en caché
cached_epg_data = {}
cached_m3u_data = []
# Contandor de intentos fallidos de descarga de la guía EPG
epg_retry_count = 0
# Fecha de la última actualización de la lista M3U
last_m3u_update = None

# ID por defecto para los canales con ID desconocido
DEFAULT_ID = "unknown"