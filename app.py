from flask import Flask, render_template, jsonify # type: ignore
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

# Ruta a los archivos
EPG_FILE = "guia.xml"
M3U_FILE = "lista.m3u"

# Función para leer el XMLTV y extraer la guía
def parse_epg():
    tree = ET.parse(EPG_FILE)
    root = tree.getroot()
    epg_data = {}
    
    for programme in root.findall("programme"):
        channel_id = programme.get("channel")
        title = programme.find("title").text if programme.find("title") is not None else "Sin título"
        start = programme.get("start")
        stop = programme.get("stop")
        epg_data.setdefault(channel_id, []).append({"title": title, "start": start, "stop": stop})
    
    return epg_data

# Función para leer la lista M3U y extraer los canales
def parse_m3u():
    # Lista con los canales encontrados
    channels = []
    with open(M3U_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/epg")
def epg():
    epg_data = parse_epg()
    channels_data = parse_m3u()
    filtered_epg = {tvg_id: epg_data.get(tvg_id, []) for tvg_id in channels_data}
    return jsonify(filtered_epg)

@app.route("/api/channels")
def channels():
    return jsonify(parse_m3u())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
