import re
import xml.etree.ElementTree as ET
from config import config
from services.utils import get_valid_logo, convert_epg_time

# Función para parsear el contenido del fichero M3U y devolver la información necesaria en una lista
def parse_m3u(m3u_content, first_run=False):
    grouped_data = {} # Diccionario para agrupar los canales por su ID
    unknown_counter = 0 # Contador para los canales sin ID

    # Parseamos el contenido del fichero M3U
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

    # Devolvemos el diccionario convertido en una lista
    return list(grouped_data.values())

# Función para parsear el contenido del fichero con la guía EPG y devolver la información necesaria en un diccionario
def parse_epg(xml_content, channel_ids):
    root = ET.fromstring(xml_content) # Nodo raíz
    epg_data = {} # Diccionario para almacenar la guía EPG

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

    return epg_data