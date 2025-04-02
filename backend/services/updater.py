import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from services.parsers import parse_m3u
from services.utils import fetch_file, save_file, load_file, convert_epg_time
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
    
    # Parseamos y almacenamos el fichero XML
    try:
        root = ET.fromstring(xml_content) # Nodo raíz
        epg_data = {} # Diccionario para almacenar la guía EPG
        
        # Extraemos los IDs de los canales presentes en la lista M3U
        channel_ids = {channel["id"] for channel in cache.cached_m3u_data}

        # Extraemos los IDs de los canales presentes en la lista M3U
        channel_ids = {channel["id"] for channel in cache.cached_m3u_data}

        # Recorremos cada elemento <programme> para extraer la información necesaria
        for programme in root.findall("programme"):
            channel_id = programme.get("channel") # ID del canal

            # Comprobamos que el programa corresponda a un canal presente en la lista M3U
            if channel_id not in channel_ids:
                continue

            title = programme.find("title").text # Título del programa
            description = programme.find("desc").text # Descripción del programa
            start = convert_epg_time(programme.get("start")) # Fecha y hora de inicio
            stop = convert_epg_time(programme.get("stop")) # Fecha y hora de finalización

            # Agregamos la información del programa al canal correspondiente
            epg_data.setdefault(channel_id, {"programs": []})["programs"].append({
                "title": title,
                "description": description,
                "since": start,
                "till": stop
            })

        # Recorremos cada elemento <channel> para extraer su logo
        for channel in root.findall("channel"):
            # Obtenemos el atributo ID del elemento <channel>
            channel_id = channel.get("id")
            # Si el canal está en la guía EPG filtrada, añadimos su logo
            if channel_id in epg_data:
                # Obtenemos el atributo src del elemento <icon>
                epg_data[channel_id]["logo"] = channel.find("icon").get("src")

        # Actualizamos la caché
        cache.cached_epg_data = epg_data
        retry_count = 0
        print("Guía EPG actualizada correctamente")

        # Si es la primera ejecución, forzamos una actualización de la lista M3U
        if first_run:
            update_m3u(force=True, skip_save=True)

    except ET.ParseError as e:
        print(f"Error al parsear la guía EPG: {e}")