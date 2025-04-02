from datetime import datetime, timedelta
from services.parsers import parse_m3u, parse_epg
from services.utils import fetch_file, save_file, load_file
from config import cache, config

# Fecha de la última actualización de la lista M3U
last_update = None

# Contador de intentos fallidos de descarga de la guía EPG
retry_count = 0

# Función para leer la lista M3U y extraer los canales
def update_m3u(first_run=False, force=False, skip_save=False):
    global last_update

    # Verificamos si se ha actualizado la lista M3U recientemente
    if not force and last_update and (datetime.now() - last_update).seconds < config.M3U_DOWNLOAD_TIMER:
        print("La lista M3U se actualizó hace menos de 1 minuto, usando caché...")
        return

    print("Intentando descargar la lista M3U...")

    # Descargamos el fichero con la lista M3U
    m3u_content = fetch_file(config.M3U_URL)

    if not m3u_content:
        # Si hubo un error pero ya está la lista en la caché, se mantiene
        if cache.cached_m3u_data:
            print("No se pudo descargar la lista M3U, usando caché...")
            return
        # Si la caché está vacía, se carga la lista del almacenamiento local
        else:
            print("No se pudo descargar la lista M3U, obteniendo copia local...")
            m3u_content = load_file(config.M3U_BACKUP)

    # Guardamos una copia del fichero
    if not skip_save:
        save_file(m3u_content, config.M3U_BACKUP)

    # Parseamos el contenido del fichero
    m3u_data = parse_m3u(m3u_content, first_run)

    # Actualizamos la caché
    cache.cached_m3u_data = m3u_data
    last_update = datetime.now()
    print("Lista M3U actualizada correctamente")

# Función para descargar la guía EPG y almacenarla en caché
def update_epg(scheduler, first_run=False):
    global retry_count

    print(f"Intentando descargar la guía EPG (intento {retry_count + 1}/{config.EPG_MAX_RETRIES + 1})...")

    # Descargamos el fichero con la guía EPG
    xml_content = fetch_file(config.EPG_URL)
    downloaded = True # Variable para controlar si los datos son descargados o locales

    if not xml_content:
        # Marcamos que se usarán datos locales (caché o almacenamiento local)
        downloaded = False

        # Si hubo un error y la caché está vacía, se carga la lista del almacenamiento local
        if not cache.cached_epg_data:
            print("No se pudo descargar la guía EPG, obteniendo copia local...")
            xml_content = load_file(config.EPG_BACKUP)
            
        # Programamos un reintento de descarga
        if (retry_count < config.EPG_MAX_RETRIES):
            retry_count += 1
            # Programamos el siguiente reintento
            delay = retry_count * config.RETRY_INCREMENT
            retry_time = datetime.now() + timedelta(minutes=delay)
            scheduler.add_job(lambda: update_epg(scheduler), "date", run_date=retry_time)
            print(f"Programando reintento {retry_count + 1}/{config.EPG_MAX_RETRIES + 1} en {delay} minutos")
        else:
            print(f"No se pudo descargar la guía EPG tras {config.EPG_MAX_RETRIES + 1} intentos fallidos")
        
        # Si hubo un error pero ya está la guía en la caché, se mantiene
        if not xml_content:
            print("No se pudo descargar la guía EPG, usando caché...")
            return
    
    # Guardamos una copia del fichero si los datos son descargados
    if downloaded:
        save_file(xml_content, config.EPG_BACKUP)

    # Extraemos los IDs de los canales presentes en la lista M3U
    channel_ids = {channel["id"] for channel in cache.cached_m3u_data}

    # Parseamos el fichero XML y lo guardamos en la caché
    cache.cached_epg_data = parse_epg(xml_content, channel_ids)
    retry_count = 0
    print("Guía EPG actualizada correctamente")

    # Si es la primera ejecución, forzamos una actualización de la lista M3U
    if first_run:
        update_m3u(force=True, skip_save=True)