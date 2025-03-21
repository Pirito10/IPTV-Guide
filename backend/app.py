from flask import Flask, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import data
import utils

# Servidor Flask
app = Flask(__name__)
CORS(app)

# Planificador de tareas
scheduler = BackgroundScheduler()

# Función para descargar la guía EPG y almacenarla en caché
def update_epg():
    print(f"Intentando descargar la guía EPG (intento {data.epg_retry_count + 1}/4)...")

    # Descargamos el archivo con la guía EPG
    xml_content = utils.fetch_file(data.EPG_URL)

    # Si hubo un error, lo reintentamos hasta 3 veces
    if not xml_content:
        if (data.epg_retry_count < 3):
            data.epg_retry_count += 1
            # Programamos el siguiente reintento
            delay = data.epg_retry_count * 30
            retry_time = datetime.now() + timedelta(minutes=delay)
            scheduler.add_job(update_epg, "date", run_date=retry_time)
            print(f"Programando reintento {data.epg_retry_count + 1}/4 en {delay} minutos")
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
            start = utils.convert_epg_time(programme.get("start")) # Fecha y hora de inicio
            stop = utils.convert_epg_time(programme.get("stop")) # Fecha y hora de finalización

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
        channel_ids = {channel["id"].split("#")[0] for channel in data.cached_m3u_data if channel["id"]}
        # Filtramos la guía EPG para obtener solo los programas de los canales presentes en la lista M3U
        filtered_epg = {id: programs for id, programs in epg_data.items() if id in channel_ids and programs}

        # Actualizamos la caché
        data.cached_epg_data = filtered_epg
        data.epg_retry_count = 0
        print("Guía EPG actualizada correctamente")

    except ET.ParseError as e:
        print(f"Error al parsear la guía EPG: {e}")

# Función para leer la lista M3U y extraer los canales
def update_m3u():
    print("Intentando descargar la lista M3U...")

    # Descargamos el archivo con la lista M3U
    m3u_content = utils.fetch_file(data.M3U_URL)

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
            id = id_match.group(1) if id_match.group(1) else data.DEFAULT_ID

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
    data.cached_m3u_data = m3u_data
    data.last_m3u_update = datetime.now()
    print("Lista M3U actualizada correctamente")

# Ruta a la API para obtener la guía EPG
@app.route("/api/epg", methods=["GET"])
def epg():
    # Devolvemos la guía almacenada en caché
     return jsonify(data.cached_epg_data)

# Ruta a la API para obtener los canales
@app.route("/api/channels", methods=["GET"])
def channels():
    # Verificamos si se ha actualizado la lista M3U en el último minuto
    if data.last_m3u_update and (datetime.now() - data.last_m3u_update).seconds < 60:
        print("La lista M3U se actualizó hace menos de 1 minuto, usando caché...")
    else:
        # Si ha pasado más de un minuto, actualizamos la lista M3U
        update_m3u()

    # Devolvemos la lista de canales almacenada en caché
    return jsonify(data.cached_m3u_data)

# Programamos la actualización de la guía EPG
scheduler.add_job(update_epg, "cron", hour="10,14,18,22", minute=0)
scheduler.start()

# Actualizamos la guía EPG y la lista M3U al iniciar la aplicación
update_epg()

# Iniciamos el servidor Flask
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()