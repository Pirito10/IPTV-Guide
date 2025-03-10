from flask import Flask, render_template, jsonify # type: ignore
import xml.etree.ElementTree as ET
import re
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# Servidor Flask
app = Flask(__name__)

# Enlaces a los archivos
EPG_URL = "https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guiatv.xml"
M3U_URL = "http://127.0.0.1:43110/1H3KoazXt2gCJgeD8673eFvQYXG7cbRddU/lista-ace.m3u"

# Variables para almacenamiento en caché
cached_epg_data = {}
cached_m3u_data = {}
# Contandor de intentos fallidos
epg_retry_count = 0
# Fecha de la última actualización de la lista M3U
last_m3u_update = None

# Planificador de tareas
scheduler = BackgroundScheduler()

# Función para descargar un archivo desde una URL
def fetch_file(url):
    try:
        response = requests.get(url, timeout=10)
        # Lanzamos una excepción si hay un error
        response.raise_for_status()
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar {url}:\n{e}\n")
        return None

# Función para descargar la guía EPG y almacenarla en caché
def update_epg():
    global cached_epg_data, epg_retry_count
    print(f"Intentando descargar la guía EPG (intento {epg_retry_count + 1}/4)...")

    # Descargamos el archivo con la guía EPG
    xml_content = fetch_file(EPG_URL)

    # Si hubo un error, lo reintentamos hasta 3 veces
    if not xml_content:
        if (epg_retry_count < 3):
            epg_retry_count += 1
            # Programamos el siguiente reintento
            delay = epg_retry_count * 30
            retry_time = datetime.now() + timedelta(minutes=delay)
            scheduler.add_job(update_epg, "date", run_date=retry_time)
            print(f"Programando reintento {epg_retry_count + 1}/4 en {delay} minutos")
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
            title = programme.find("title").text if programme.find("title") is not None else "Sin título" # Título del programa
            start = programme.get("start")[:14] # Fecha y hora de inicio
            stop = programme.get("stop")[:14] # Fecha y hora de finalización

            # Agregamos la información al diccionario agrupada por canal
            epg_data.setdefault(channel_id, []).append({
                "title": title,
                "start": start,
                "stop": stop
            })
        
        # Actualizamos la lista M3U
        update_m3u()
        # Extraemos los IDs de los canales presentes en la lista M3U
        channel_ids = {channel["tvg_id"] for channel in cached_m3u_data if channel["tvg_id"]}
        # Filtramos la guía EPG para obtener solo los programas de los canales presentes en la lista M3U
        filtered_epg = {tvg_id: epg_data.get(tvg_id, []) for tvg_id in channel_ids}
        # Actualizamos la caché
        cached_epg_data = filtered_epg
        epg_retry_count = 0
        print("Guía EPG actualizada correctamente")

    except ET.ParseError as e:
        print(f"Error al parsear la guía EPG: {e}")

# Función para leer la lista M3U y extraer los canales
def update_m3u():
    global cached_m3u_data, last_m3u_update
    print("Intentando descargar la lista M3U...")

    # Descargamos el archivo con la lista M3U
    m3u_content = fetch_file(M3U_URL)

    # Si hubo un error, se mantiene la caché
    if not m3u_content:
        print("No se pudo descargar la lista M3U")
        return
    
    m3u_data = [] # Diccionario para almacenar los canales

    # Parseamos y almacenamos el archivo M3U
    lines = m3u_content.splitlines()
    for i in range(len(lines)):
        # Leemos la línea con la información del canal
        if lines[i].startswith("#EXTINF"):
            # Extraemos los datos con expresiones regulares
            logo_match = re.search(r'tvg-logo="(.*?)"', lines[i]) # URL del logo
            logo_url = logo_match.group(1) if logo_match else ""
            tvg_id_match = re.search(r'tvg-id="(.*?)"', lines[i]) # ID del canal
            tvg_id = tvg_id_match.group(1) if tvg_id_match else ""
            group_match = re.search(r'group-title="(.*?)"', lines[i]) # Grupo del canal
            group = group_match.group(1) if group_match else ""
            name_match = re.search(r',(.+)$', lines[i].strip()) # Nombre del canal
            channel_name = name_match.group(1) if name_match else ""

            # Extraemos la URL de la siguiente línea
            url = lines[i + 1].strip() if i + 1 < len(lines) else ""
            
            # Agregamos el canal al diccionario
            m3u_data.append({
                "tvg_id": tvg_id,
                "name": channel_name,
                "group": group,
                "logo": logo_url,
                "url": url
            })

    # Actualizamos la caché
    cached_m3u_data = m3u_data
    last_m3u_update = datetime.now()
    print("Lista M3U actualizada correctamente")

# Ruta a la página principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta a la API para obtener la guía EPG
@app.route("/api/epg")
def epg():
    # Devolvemos la guía almacenada en caché
     return jsonify(cached_epg_data)

# Ruta a la API para obtener los canales
@app.route("/api/channels")
def channels():
    global last_m3u_update

    # Verificamos si se ha actualizado la lista M3U en el último minuto
    if last_m3u_update and (datetime.now() - last_m3u_update).seconds < 60:
        print("La lista M3U se actualizó hace menos de 1 minuto, usando caché...")
    else:
        # Si ha pasado más de un minuto, actualizamos la lista M3U
        update_m3u()

    # Devolvemos la lista de canales almacenada en caché
    return jsonify(cached_m3u_data)

# Programamos la actualización de la guía EPG
scheduler.add_job(update_epg, "cron", hour="10,14,18,22", minute=0)
scheduler.start()

# Actualizamos la guía EPG y la lista M3U al iniciar la aplicación
update_epg()

# Iniciamos el servidor Flask
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=3333, debug=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()