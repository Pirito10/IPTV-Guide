import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from services.utils import fetch_file, save_file, convert_epg_time, get_valid_logo
from config import cache, config

# Fecha de la última actualización de la lista M3U
last_update = None

# Contador de intentos fallidos de descarga de la guía EPG
retry_count = 0

# Función para leer la lista M3U y extraer los canales
def update_m3u(first_run=False, force=False):
    global last_update

    # Verificamos si se ha actualizado la lista M3U recientemente
    if not force and last_update and (datetime.now() - last_update).seconds < config.M3U_DOWNLOAD_TIMER:
        print("La lista M3U se actualizó hace menos de 1 minuto, usando caché...")
        return

    print("Intentando descargar la lista M3U...")

    # Descargamos el fichero con la lista M3U
    m3u_content = fetch_file(config.M3U_URL)

    # Si hubo un error, se mantiene la caché
    if not m3u_content:
        print("No se pudo descargar la lista M3U")
        return
    
    # Guardamos una copia del fichero
    save_file(m3u_content, "m3u_backup.m3u")
    
    grouped_data = {} # Diccionario para agrupar los canales por su ID
    unknown_counter = 0 # Contador para los canales sin ID

    # Parseamos y almacenamos el fichero M3U
    lines = m3u_content.splitlines()
    for i in range(len(lines)):
        # Leemos la línea con la información del canal y extraemos los datos con regex
        if lines[i].startswith("#EXTINF"):
            # ID del canal
            id_match = re.search(r'tvg-id="(.*?)"', lines[i])
            if id_match.group(1):
                id = id_match.group(1)
            # Si el canal no tiene ID, le asignamos uno por defecto junto con un contador
            else:
                unknown_counter += 1
                id = f"{config.DEFAULT_ID}#{unknown_counter}"

            # URL del logo
            logo_match = re.search(r'tvg-logo="(.*?)"', lines[i])
            logo = logo_match.group(1)

            # Grupo del canal
            group_match = re.search(r'group-title="(.*?)"', lines[i])
            group = group_match.group(1)

            # Nombre del canal
            name_match = re.search(r', (.+)$', lines[i])
            name = name_match.group(1)

            # Extraemos la URL de la siguiente línea
            url = lines[i + 1].removeprefix("acestream://")

            # Si el ID no está en el diccionario, agregamos toda la información del canal
            if id not in grouped_data:
                grouped_data[id] = {
                    "id": id,
                    "logo": get_valid_logo(id, logo) if not first_run else logo,
                    "group": group,
                    "streams": [{
                        "name": name,
                        "url": url
                    }]
                }
            # Si ya existe, agregamos solo la información del stream
            else:
                grouped_data[id]["streams"].append({
                    "name": name,
                    "url": url
                })

    # Convertimos el diccionario en una lista
    m3u_data = list(grouped_data.values())

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

    # Si hubo un error, lo reintentamos
    if not xml_content:
        if (retry_count < config.EPG_MAX_RETRIES):
            retry_count += 1
            # Programamos el siguiente reintento
            delay = retry_count * config.RETRY_INCREMENT
            retry_time = datetime.now() + timedelta(minutes=delay)
            scheduler.add_job(lambda: update_epg(scheduler), "date", run_date=retry_time)
            print(f"Programando reintento {retry_count + 1}/{config.EPG_MAX_RETRIES + 1} en {delay} minutos")
        else:
            print(f"No se pudo descargar la guía EPG tras {config.EPG_MAX_RETRIES + 1} intentos fallidos")
        return
    
    # Guardamos una copia del fichero
    save_file(xml_content, "epg_backup.xml")
    
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
            update_m3u(force=True)

    except ET.ParseError as e:
        print(f"Error al parsear la guía EPG: {e}")