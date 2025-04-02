import re
from config import config
from services.utils import get_valid_logo

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