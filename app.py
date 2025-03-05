from flask import Flask, render_template, jsonify # type: ignore
import xml.etree.ElementTree as ET
import re
import requests

app = Flask(__name__)

# Ruta a los archivos
EPG_URL = "https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guiatv.xml"
M3U_URL = "https://proxy.zeronet.dev/1H3KoazXt2gCJgeD8673eFvQYXG7cbRddU/lista-ace.m3u"

# Función para descargar un archivo desde una URL
def fetch_file(url):
    try:
        response = requests.get(url, timeout=10)  # 10 segundos de timeout
        response.raise_for_status()  # Lanza una excepción si hay un error
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar {url}: {e}")
        return None

# Función para leer la guía EPG y extraer los programas
def parse_epg():
    epg_data = {}  # Diccionario donde almacenaremos la información
    xml_content = fetch_file(EPG_URL)
    if not xml_content:
        return epg_data
    
    try:
        root = ET.fromstring(xml_content)  # Nodo raíz
        for programme in root.findall("programme"):  # Recorremos cada elemento <programme>
            channel_id = programme.get("channel")  # Extraemos el ID del canal
            title = programme.find("title").text if programme.find("title") is not None else "Sin título" # Extraemos el título del programa
            start = programme.get("start")[:14]  # Extraemos la fecha y hora de inicio
            stop = programme.get("stop")[:14]  # Extraemos la fecha y hora de finalización

            # Agregamos la información al diccionario agrupada por canal
            epg_data.setdefault(channel_id, []).append({
                "title": title,
                "start": start,
                "stop": stop
            })
    except ET.ParseError as e:
        print(f"Error al parsear el XML: {e}")
        
    return epg_data

# Función para leer la lista M3U y extraer los canales
def parse_m3u():
    # Lista con los canales encontrados
    channels = []
    m3u_content = fetch_file(M3U_URL)
    if not m3u_content:
        return channels
    
    lines = m3u_content.splitlines()

    for i in range(len(lines)):
        # Leemos la línea con la información del canal
        if lines[i].startswith("#EXTINF"):
            # Extraemos los datos con expresiones regulares
            logo_match = re.search(r'tvg-logo="(.*?)"', lines[i])
            tvg_id_match = re.search(r'tvg-id="(.*?)"', lines[i])
            group_match = re.search(r'group-title="(.*?)"', lines[i])
            name_match = re.search(r',(.+)$', lines[i].strip())
            
            logo_url = logo_match.group(1) if logo_match else ""
            tvg_id = tvg_id_match.group(1) if tvg_id_match else ""
            group = group_match.group(1) if group_match else ""
            channel_name = name_match.group(1) if name_match else ""
            # Extraemos la URL de la siguiente línea
            url = lines[i + 1].strip() if i + 1 < len(lines) else ""
            
            channels.append({
                "tvg_id": tvg_id,
                "name": channel_name,
                "group": group,
                "logo": logo_url,
                "url": url
            })
    return channels

# Ruta a la página principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta a la API para obtener la guía EPG
@app.route("/api/epg")
def epg():
    # Parseamos la guía EPG y la lista M3U
    epg_data = parse_epg()
    channels_data = parse_m3u()
    # Extraemos los IDs de los canales presentes en la lista M3U
    channel_ids = [channel["tvg_id"] for channel in channels_data if channel["tvg_id"]]
    # Filtramos la guía EPG para obtener solo los programas de los canales presentes en la lista M3U
    filtered_epg = {tvg_id: epg_data.get(tvg_id, []) for tvg_id in channel_ids}
    return jsonify(filtered_epg)

# Ruta a la API para obtener los canales
@app.route("/api/channels")
def channels():
    return jsonify(parse_m3u())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
