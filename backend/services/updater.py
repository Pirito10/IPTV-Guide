import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from services.utils import fetch_file, convert_epg_time
from config import cache, config

# Fecha de la última actualización de la lista M3U
last_update = None

# Función para leer la lista M3U y extraer los canales
def update_m3u():
    global last_update

    # Verificamos si se ha actualizado la lista M3U en el último minuto
    if last_update and (datetime.now() - last_update).seconds < 60:
        print("La lista M3U se actualizó hace menos de 1 minuto, usando caché...")
        return

    print("Intentando descargar la lista M3U...")

    # Descargamos el archivo con la lista M3U
    m3u_content = fetch_file(config.M3U_URL)

    # Si hubo un error, se mantiene la caché
    if not m3u_content:
        print("No se pudo descargar la lista M3U")
        return
    
    m3u_data = [] # Lista para almacenar los canales
    id_counter = {} # Diccionario para almacenar un contador para cada ID de canal

    # Parseamos y almacenamos el archivo M3U
    lines = m3u_content.splitlines()
    for i in range(len(lines)):
        # Leemos la línea con la información del canal y extraemos los datos con regex
        if lines[i].startswith("#EXTINF"):
            # ID del canal
            id_match = re.search(r'tvg-id="(.*?)"', lines[i])
            id = id_match.group(1) if id_match.group(1) else config.DEFAULT_ID

            # Incrementamos el contador para el ID del canal
            id_counter.setdefault(id, 0)
            id_counter[id] += 1
            # Establecemos el ID con formato "ID#N"
            id = f"{id}#{id_counter[id]}"

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
            
            # Agregamos el canal al diccionario
            m3u_data.append({
                "id": id,
                "name": name,
                "group": group,
                "logo": logo,
                "url": url
            })

    # Actualizamos la caché
    cache.cached_m3u_data = m3u_data
    last_update = datetime.now()
    print("Lista M3U actualizada correctamente")

    # TODO si no se descargó la lista de canales, la guía EPG queda vacía (no hay canales por los que filtrar) y hay que esperar al timer para que se intente de nuevo

# Función para descargar la guía EPG y almacenarla en caché
def update_epg(scheduler):
    # TODO testar esto
    retry_count = 0 # Contandor de intentos fallidos de descarga de la guía EPG

    print(f"Intentando descargar la guía EPG (intento {retry_count + 1}/4)...")

    # Descargamos el archivo con la guía EPG
    xml_content = fetch_file(config.EPG_URL)

    # Si hubo un error, lo reintentamos hasta 3 veces
    if not xml_content:
        if (retry_count < 3):
            retry_count += 1
            # Programamos el siguiente reintento
            delay = retry_count * 30
            retry_time = datetime.now() + timedelta(minutes=delay)
            scheduler.add_job(update_epg, "date", run_date=retry_time)
            print(f"Programando reintento {retry_count + 1}/4 en {delay} minutos")
        else:
            print("No se pudo descargar la guía EPG tras 4 intentos fallidos")
        return
    
    # Parseamos y almacenamos el archivo XML
    try:
        epg_data = {} # Diccionario para almacenar la guía EPG
        root = ET.fromstring(xml_content) # Nodo raíz

        # Recorremos cada elemento <programme>
        for programme in root.findall("programme"):
            # Extraemos la información necesaria
            channel_id = programme.get("channel") # ID del canal
            title = programme.find("title").text # Título del programa
            description = programme.find("desc").text # Descripción del programa
            start = convert_epg_time(programme.get("start")) # Fecha y hora de inicio
            stop = convert_epg_time(programme.get("stop")) # Fecha y hora de finalización

            # Agregamos la información al diccionario agrupada por canal
            epg_data.setdefault(channel_id, []).append({
                "title": title,
                "description": description,
                "since": start,
                "till": stop
            })
        
        # Actualizamos la lista M3U
        update_m3u()

        # Extraemos los IDs de los canales presentes en la lista M3U, sin el contador
        channel_ids = {channel["id"].split("#")[0] for channel in cache.cached_m3u_data if channel["id"]}
        # Filtramos la guía EPG para obtener solo los programas de los canales presentes en la lista M3U
        filtered_epg = {id: programs for id, programs in epg_data.items() if id in channel_ids and programs}

        # Actualizamos la caché
        cache.cached_epg_data = filtered_epg
        retry_count = 0
        print("Guía EPG actualizada correctamente")

    except ET.ParseError as e:
        print(f"Error al parsear la guía EPG: {e}")