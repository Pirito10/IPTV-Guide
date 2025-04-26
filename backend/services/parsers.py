import re
import xml.etree.ElementTree as ET
from config import config
from services.logger import logger
from services.utils import get_valid_logo, convert_epg_time

# Función para parsear el contenido del fichero M3U y devolver la información necesaria en una lista
def parse_m3u(m3u_content, first_run=False):
    grouped_data = {} # Diccionario para agrupar los canales por su ID
    unknown_channels = 0 # Contador para los canales sin ID

    logger.info(f"Parsing M3U list content (first run: {first_run})...")

    # Parseamos el contenido del fichero M3U
    lines = m3u_content.splitlines()
    for i in range(len(lines)):
        # Leemos la línea con la información del canal y extraemos los datos con regex
        if lines[i].startswith("#EXTINF"):
            # ID del canal
            id_match = re.search(r'tvg-id="(.*?)"', lines[i])
            if id_match.group(1):
                id = id_match.group(1)
                logger.debug(f"Channel found with ID: {id}")
            # Si el canal no tiene ID, le asignamos uno por defecto junto con un contador
            else:
                unknown_channels += 1
                id = f"{config.DEFAULT_ID}#{unknown_channels}"
                logger.warning(f"Channel found without ID, using default ID: {id}")

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
                logger.debug(f"Channel created: {grouped_data[id]}")

            # Si ya existe, agregamos solo la información del stream
            else:
                grouped_data[id]["streams"].append({
                    "name": name,
                    "url": url
                })
                logger.debug(f"Channel already exists, added new stream URL: {grouped_data[id]}")

    logger.info(f"M3U list parsed successfully, found {len(grouped_data)} channels")

    # Devolvemos el diccionario convertido en una lista
    return list(grouped_data.values())


# Función para parsear el contenido del fichero con la guía EPG y devolver la información necesaria en un diccionario
def parse_epg(xml_content, channel_ids):
    root = ET.fromstring(xml_content) # Nodo raíz
    epg_data = {} # Diccionario para almacenar la guía EPG

    logger.info("Parsing EPG content...")

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

        if not start or not stop:
            logger.warning(f"Invalid start/stop time for program: {title} ({channel_id})")
            continue

        # Agregamos la información del programa al canal correspondiente
        epg_data.setdefault(channel_id, {"programs": []})["programs"].append({
            "title": title,
            "description": description,
            "since": start,
            "till": stop
        })
        logger.debug(f"Program added: {title} ({channel_id})")

    # Recorremos cada elemento <channel> para extraer su logo
    for channel in root.findall("channel"):
        # Obtenemos el atributo ID del elemento <channel>
        channel_id = channel.get("id")
        # Si el canal está en la guía EPG filtrada, añadimos su logo
        if channel_id in epg_data:
            # Buscamos el elemento <icon> dentro del canal
            icon = channel.find("icon")
            if icon is not None:
                # Obtenemos el atributo src del elemento <icon>
                epg_data[channel_id]["logo"] = icon.get("src")
                logger.debug(f"Logo added: {epg_data[channel_id]['logo']} ({channel_id})")
            else:
                logger.debug(f"No logo found ({channel_id})")

    logger.info(f"EPG parsed successfully, found programs for {len(epg_data)} channels")

    return epg_data