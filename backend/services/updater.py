from datetime import datetime, timedelta
from services.parsers import parse_m3u, parse_epg
from services.utils import fetch_file, save_file, load_file
from config import cache, config
from services.logger import logger

# Fecha de la última actualización de la lista M3U
last_update = None

# Contador de intentos fallidos de descarga de la guía EPG
retry_count = 0

# Función para leer la lista M3U y extraer los canales
def update_m3u(first_run=False, force=False, skip_save=False):
    global last_update

    logger.info("Starting M3U list update...")

    # Verificamos si se ha actualizado la lista M3U recientemente
    recently_updated = last_update and (datetime.now() - last_update).seconds < config.M3U_DOWNLOAD_TIMER
    if not force and recently_updated:
        logger.info("M3U list recently updated, skipping update")
        return

    # Descargamos el fichero con la lista M3U
    m3u_content = fetch_file(config.M3U_URL)
    downloaded = True # Variable para controlar si los datos son descargados o locales

    if not m3u_content:
        # Marcamos que se usarán datos locales (caché o almacenamiento local)
        downloaded = False
        
        # Si hubo un error pero ya está la lista en la caché, se mantiene
        if cache.cached_m3u_data:
            logger.warning("Failed to download M3U list file, using cache...")
            return
        # Si la caché está vacía, se carga la lista del almacenamiento local
        else:
            logger.warning("Failed to download M3U list file, using local backup...")
            m3u_content = load_file(config.M3U_BACKUP)

    # Guardamos una copia del fichero si los datos son descargados
    if downloaded and not skip_save:
        save_file(m3u_content, config.M3U_BACKUP)

    # Parseamos el fichero M3U y lo guardamos en la caché
    cache.cached_m3u_data = parse_m3u(m3u_content, first_run)
    last_update = datetime.now()

    logger.info("M3U list cache updated")


# Función para descargar la guía EPG y almacenarla en caché
def update_epg(scheduler, first_run=False):
    global retry_count

    logger.info("Starting EPG update (attempt %d/%d)...", retry_count + 1, config.EPG_MAX_RETRIES + 1)

    # Descargamos el fichero con la guía EPG
    xml_content = fetch_file(config.EPG_URL)
    downloaded = True # Variable para controlar si los datos son descargados o locales

    if not xml_content:
        # Marcamos que se usarán datos locales (caché o almacenamiento local)
        downloaded = False

        # Programamos un reintento de descarga
        if (retry_count < config.EPG_MAX_RETRIES):
            retry_count += 1
            # Programamos el siguiente reintento
            delay = retry_count * config.RETRY_INCREMENT
            retry_time = datetime.now() + timedelta(minutes=delay)
            scheduler.add_job(lambda: update_epg(scheduler), "date", run_date=retry_time)
            logger.warning("Retrying EPG update in %d minutes", delay)
        else:
            logger.error("Failed to download EPG file after %d failed attempts", config.EPG_MAX_RETRIES + 1)

        # Si hubo un error y la caché está vacía, se carga la lista del almacenamiento local
        if not cache.cached_epg_data:
            logger.warning("Failed to download EPG file, using local backup...")
            xml_content = load_file(config.EPG_BACKUP)

        # Si hubo un error pero ya está la guía en la caché, se mantiene
        if not xml_content:
            logger.warning("Failed to download EPG file, using cache...")
            return
    else:
        # Reiniciamos el contador de reintentos si la descarga fue exitosa
        retry_count = 0
    
    # Guardamos una copia del fichero si los datos son descargados
    if downloaded:
        save_file(xml_content, config.EPG_BACKUP)

    # Extraemos los IDs de los canales presentes en la lista M3U
    channel_ids = {channel["id"] for channel in cache.cached_m3u_data}

    # Parseamos el fichero XML y lo guardamos en la caché
    cache.cached_epg_data = parse_epg(xml_content, channel_ids)

    logger.info("EPG cache updated")

    # Si es la primera ejecución, forzamos una actualización de la lista M3U
    if first_run:
        logger.info("Forcing M3U update after initial EPG load")
        update_m3u(force=True, skip_save=True)