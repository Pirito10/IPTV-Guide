import cache
from updater import update_m3u
from datetime import datetime
from flask import jsonify, Blueprint

routes = Blueprint("routes", __name__)

# Ruta a la API para obtener los canales
@routes.route("/api/channels")
def channels():
    # Verificamos si se ha actualizado la lista M3U en el último minuto
    if cache.last_m3u_update and (datetime.now() - cache.last_m3u_update).seconds < 60:
        print("La lista M3U se actualizó hace menos de 1 minuto, usando caché...")
    else:
        # Si ha pasado más de un minuto, actualizamos la lista M3U
        update_m3u()

    # Devolvemos la lista de canales almacenada en caché
    return jsonify(cache.cached_m3u_data)

# Ruta a la API para obtener la guía EPG
@routes.route("/api/epg")
def epg():
    # Devolvemos la guía almacenada en caché
    return jsonify(cache.cached_epg_data)