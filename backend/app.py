from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
import data
import updater

# Servidor Flask
app = Flask(__name__)
CORS(app)

# Planificador de tareas
scheduler = BackgroundScheduler()

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
        updater.update_m3u()

    # Devolvemos la lista de canales almacenada en caché
    return jsonify(data.cached_m3u_data)

# Programamos la actualización de la guía EPG
scheduler.add_job(partial(updater.update_epg, scheduler), "cron", hour="10,14,18,22", minute=0)
scheduler.start()

# Actualizamos la guía EPG y la lista M3U al iniciar la aplicación
updater.update_epg(scheduler)

# Iniciamos el servidor Flask
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()