from flask import jsonify, Blueprint
from services.logger import logger
from services.updater import update_m3u
from config import cache

routes = Blueprint("routes", __name__)

# Ruta a la API para obtener los canales
@routes.route("/api/channels")
def channels():
    logger.info("Request to /api/channels received")
    # Intentamos actualizar la lista M3U
    update_m3u()

    # Devolvemos la lista de canales almacenada en caché
    return jsonify(cache.cached_m3u_data)

# Ruta a la API para obtener la guía EPG
@routes.route("/api/epg")
def epg():
    logger.info("Request to /api/epg received")
    # Devolvemos la guía almacenada en caché
    return jsonify(cache.cached_epg_data)