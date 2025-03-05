from flask import Flask, render_template, jsonify
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

# Función para leer la lista M3U y extraer solo los canales
def parse_m3u():
    channels = {}
    with open(M3U_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                match = re.search(r'tvg-id="(.*?)"', lines[i])
                tvg_id = match.group(1) if match else None
                name_match = re.search(r',(.+)$', lines[i].strip())
                channel_name = name_match.group(1) if name_match else "Desconocido"
                url = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if tvg_id:
                    channels[tvg_id] = {"name": channel_name, "url": url}
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
    app.run(host="0.0.0.0", port=5000, debug=True)
