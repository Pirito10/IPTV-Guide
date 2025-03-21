# Variables para almacenamiento en caché
cached_epg_data = {}
cached_m3u_data = []

# Contandor de intentos fallidos de descarga de la guía EPG
epg_retry_count = 0

# Fecha de la última actualización de la lista M3U
last_m3u_update = None